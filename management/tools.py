import datetime
from django.core.mail import EmailMultiAlternatives
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcms.request.v20190101.DescribeMetricListRequest import DescribeMetricListRequest
import json
import requests
from django.utils import timezone

from blog.models import Article, Category, Tag, Section, Note
from management.models import WebsiteConfig
from myblog.settings import BAIDU_USERNAME, BAIDU_PASSWORD, BAIDU_TOKEN, BAIDU_ID, BAIDU_START_DATE
from myblog.settings import ALIYUN_INSTANCE, ALIYUN_KEYId, ALIYUN_LOCATION, ALIYUN_SECRET


# 发送邮件验证码
def sendEmail(receive, username, action, code):
    """
    :param str receive: 收件人
    :param str username: 收件人用户名
    :param str action: 操作内容
    :param str code: 验证码
    :return: 1 发送成功
    """
    content = """
    <body style="background-color: #ebedf0;margin: 0;padding: 0">
        <div id="content" style="width: 75%;margin: 10% auto;background-color: white;border-radius: 10px;box-shadow: 0 0 15px 1px rgba(0, 0, 0, 0.4);">
            <div style="text-align: center;background-color: #ecf0f1;height: 80px">
                <h2 style="margin: 0 auto;line-height: 80px;">【崔亮的博客】验证码</h2>
            </div>
            <div style="padding: 0 20px;">
                <p style="font-weight: bold">尊敬的""" + username + """：您好！</p>
                <p style="text-indent:2em;font-weight: bold">您正在进行
                    <span style="color: #e74c3c">""" + action + """</span>操作，请在验证码输入框输入：
                    <span style="color: #e74c3c;font-weight: bold;font-size: 40px">""" + code + """</span>，以完成操作，验证码有效期为3分钟。
                </p>
                <br>
                <p style="color: #bdc3c7;text-indent:2em">注意：此操作可能会对您的账号进行""" + action + """操作。
                    如非本人操作，请及时登录并修改密码以保证账户安全，请勿泄露此验证码！</p>
            </div>
            <div style="background-color: #ecf0f1;padding: 20px;">
                <p style="color: #bdc3c7;text-indent:2em;margin: 0 auto;line-height: 30px">您会收到这封邮件，是由于在
                    <a href="https://www.cuiliangblog.cn" style="text-decoration: none">崔亮的博客</a>
                    进行了新用户注册或修改密码、绑定邮箱等操作。如果您并没有访问过
                    <a href="https://www.cuiliangblog.cn" style="text-decoration: none">崔亮的博客</a>
                    ，或没有进行上述操作， 请忽略这封邮件！
                </p>
            </div>
        </div>
        <script>
            var width = document.body.clientWidth;
            if (width < 500) {
                document.querySelector("#content").style.width="95%"
            }
        </script>
    </body>
    """
    subject = "[崔亮的博客] Email 验证码"
    from_email = "崔亮的博客<cuiliangblog@qq.com>"
    msg = EmailMultiAlternatives(subject, content, from_email, [receive])
    msg.content_subtype = "html"
    return msg.send()


# 百度统计api
class BaiduApi:
    def __init__(self):
        self.url = 'https://api.baidu.com/json/tongji/v1/ReportService/getData'
        self.username = BAIDU_USERNAME
        self.password = BAIDU_PASSWORD
        self.token = BAIDU_TOKEN
        self.id = BAIDU_ID

    # 获取所有流量统计
    def countAll(self):
        end_date = (timezone.now()).strftime('%Y%m%d')
        data = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": BAIDU_START_DATE,
                "end_date": end_date,
                "metrics": "pv_count,visitor_count,ip_count",
                "method": "trend/time/a",
                "area": ""
            }
        }
        try:
            r = requests.post(self.url, data=json.dumps(data))
            result = json.loads(r.text)
            pv = result["body"]["data"][0]["result"]["pageSum"][0][0]
            uv = result["body"]["data"][0]["result"]["pageSum"][0][1]
            ip = result["body"]["data"][0]["result"]["pageSum"][0][2]
            count_dict = {}
            count_dict['pv'] = pv
            count_dict['uv'] = uv
            count_dict['ip'] = ip
        except Exception as e:
            print(e)
            count_dict = {}
            count_dict['pv'] = 8024
            count_dict['uv'] = 3025
            count_dict['ip'] = 2896
        return count_dict

    # 获取当天流量统计和昨天对比
    def countToday(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
        data = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": today,
                "end_date": today,
                "metrics": "pv_count,visitor_count,avg_visit_time,avg_visit_pages",
                "method": "trend/time/a",
                "start_date2": yesterday,
                "end_date2": yesterday,
                "area": ""
            }
        }
        r = requests.post(self.url, data=json.dumps(data))
        result = json.loads(r.text)["body"]["data"][0]["result"]["pageSum"]
        return result

    # 近7天流量趋势
    def countTrend(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        weekago = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y%m%d")
        data = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": weekago,
                "end_date": today,
                "metrics": "pv_count,visitor_count,new_visitor_count,ip_count,avg_visit_time,avg_visit_pages",
                "method": "trend/time/a",
                "gran": "day",
                "area": ""
            }
        }
        r = requests.post(self.url, data=json.dumps(data))
        result = json.loads(r.text)["body"]["data"][0]["result"]
        return result

    # 受访页统计
    def countPage(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        weekago = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y%m%d")
        data = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": weekago,
                "end_date": today,
                "metrics": "pv_count,visitor_count,visit1_count,average_stay_time",
                "method": "visit/toppage/a",
                "max_results": "5"
            }
        }
        r = requests.post(self.url, data=json.dumps(data))
        result = json.loads(r.text)["body"]["data"][0]["result"]
        return result

    # 用户设备统计:
    def countDevice(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        weekago = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y%m%d")
        data_pc = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": weekago,
                "end_date": today,
                "metrics": "pv_count",
                "method": "trend/time/a",
                "clientDevice": "pc",
                "gran": "day",
                "area": ""
            }
        }
        r_pc = requests.post(self.url, data=json.dumps(data_pc))
        result_pc = json.loads(r_pc.text)["body"]["data"][0]["result"]["pageSum"][0]
        data_mobile = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": weekago,
                "end_date": today,
                "metrics": "pv_count",
                "method": "trend/time/a",
                "clientDevice": "mobile",
                "gran": "day",
                "area": ""
            }
        }
        r_mobile = requests.post(self.url, data=json.dumps(data_mobile))
        result_mobile = json.loads(r_mobile.text)["body"]["data"][0]["result"]["pageSum"][0]
        data = {}
        data['pc'] = result_pc[-1]
        data['mobile'] = result_mobile[-1]
        return data

    # 用户区域统计:
    def countMap(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        weekago = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y%m%d")
        data = {
            "header": {
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "account_type": 1
            },
            "body": {
                "site_id": self.id,
                "start_date": weekago,
                "end_date": today,
                "metrics": "pv_count,pv_ratio",
                "method": "visit/district/a",
            }
        }
        r = requests.post(self.url, data=json.dumps(data))
        result = json.loads(r.text)["body"]["data"][0]["result"]
        return result


# 阿里云sdk
class AliyunSDK:
    def __init__(self, metric):
        self.accessKeyId = ALIYUN_KEYId
        self.accessSecret = ALIYUN_SECRET
        self.location = ALIYUN_LOCATION
        self.instanceId = ALIYUN_INSTANCE
        self.metric = metric

    def metricInfo(self):
        startTime = (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            print(self.accessKeyId)
            print(self.accessSecret)
            print(self.location)
            print(self.instanceId)
            print(self.metric)
            client = AcsClient(self.accessKeyId, self.accessSecret, self.location)
            request = DescribeMetricListRequest()
            request.set_accept_format('json')
            request.set_StartTime(startTime)
            instance = "{\"instanceId\":\"" + self.instanceId + "\"}"
            request.set_Dimensions(instance)
            request.set_Period("60")
            request.set_Namespace("acs_ecs_dashboard")
            request.set_MetricName(self.metric)
            response = client.do_action_with_exception(request)
            result = str(response, encoding='utf-8')
            result_dict = json.loads(result)
            print(result_dict)
            if result_dict['Code'] == '200':
                data = eval(result_dict['Datapoints'][1:-1])
                return data[0]["Average"]
        except Exception as e:
            print(e)
            value = 0.00
            return value


# sitemap生成
class SiteMap:
    def __init__(self):
        self.domain = WebsiteConfig.objects.get(id=1).domain
        self.url = []

    # 生成博文链接
    def articleUrl(self):
        article_all = Article.objects.all()
        for article in article_all:
            article_url = self.domain + "blog/show-" + str(article.id) + "/"
            self.url.append(article_url)

    # 生成博文分类链接
    def categoryUrl(self):
        category_all = Category.objects.all()
        for category in category_all:
            category_url = self.domain + "blog/category-" + str(category.id) + "/"
            self.url.append(category_url)

    # 生成博文标签链接
    def tagUrl(self):
        tag_all = Tag.objects.all()
        for tag in tag_all:
            tag_url = self.domain + "blog/tag-" + str(tag.id) + "/"
            self.url.append(tag_url)

    # 生成笔记链接
    def sectionUrl(self):
        section_all = Section.objects.all()
        for section in section_all:
            section_url = self.domain + "blog/section-" + str(section.id) + "/"
            self.url.append(section_url)

    # 生成笔记目录链接
    def noteUrl(self):
        note_all = Note.objects.all()
        for note in note_all:
            note_url = self.domain + "blog/note-" + str(note.id) + "/"
            self.url.append(note_url)

    # 生成其他链接
    def otherUrl(self):
        self.url.append(self.domain + "blog/timeAxis/")
        self.url.append(self.domain + "blog/about/")
        self.url.append(self.domain + "blog/messageBoard/")
