package util

import (
	"testing"
	//"net/http"
	"strconv"
	"net/http"
	"time"
	"strings"
	"fmt"
	"io/ioutil"
)

func TestCreateAdzone(t *testing.T) {

}

// 创建推广位
func TestAddPID(t *testing.T) {

	volume := 1                // 推广位数量
	tbToken := "575f5f0eee315" // 淘宝token
	gcid := 8
	siteID := "546500150" // 导购ID
	cookie := "t=e519644672d288d46608a40d41b08cbd; cna=zKt/FNr76gACAXTmgpadK+TX; 437160025_yxjh-filter-1=true; account-path-guide-s1=true; cookie2=14c7c1e2f50bc4a410ad04afe438e064; v=0; _tb_token_=575f5f0eee315; cookie32=91a90104d2fe992235a1b25ab71f12db; cookie31=NDM3MTYwMDI1LGIxNTk3NTM1NCwzODYyMDQxNzRAcXEuY29tLFRC; 437160025-payment-time=true; alimamapwag=TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfNikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc1LjAuMzc3MC45MCBTYWZhcmkvNTM3LjM2; alimamapw=BgNWDFFTVwMFPwcDAFcOBwYFVFBWAl9UB1ABVQQBV1BaVwYDAgZSUQME; taokeisb2c=; login=V32FPkk%2Fw0dUvg%3D%3D; JSESSIONID=1BA5E27CECC361521D3FF95C7CB7E965; apush4ffe71c03abb40173dc3d566a9c6e6eb=%7B%22ts%22%3A1560683614753%2C%22heir%22%3A1560683346648%2C%22parentId%22%3A1560682464203%7D; l=bBQRY45uvqCWP_LjBOfwVuI8arbtrpOX5sPzw4_GVIB19GWjCKDVFHwQIGsyN3Q_E_5poF-zvtIGSRFD5zaT-x1..; isg=BNXVIx86JBLnaQGTRA83voLY5NdPeomCQnrloFd12MjLrt2gGCCltnAoePK9rqGc"
	pvid := "10_116.231.51.205_7674_1560682524267"

	url := "https://pub.alimama.com/common/adzone/selfAdzoneCreate.json"

	for i := 0; i < volume; i++ {

		adzoneName := "tg" + strconv.Itoa(i)
		payload := strings.NewReader(fmt.Sprintf("tag=28&gcid=%d&siteid=%s&selectact=add&newadzonename=%s&t=%d&pvid=%s&_tb_token=%s",
			gcid, siteID, adzoneName, time.Now().Unix(), pvid, tbToken))

		req, err := http.NewRequest("POST", url, payload)
		if err != nil {
			t.Fatal(err.Error())
		}
		req.Header.Add("Host", "pub.alimama.com")
		req.Header.Add("Content-Length", strconv.Itoa(payload.Len()))
		req.Header.Add("Accept", "application/json, text/javascript, */*; q=0.01")
		req.Header.Add("Accept-Encoding", "gzip, deflate")
		req.Header.Add("Accept-Language", "zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2")
		req.Header.Add("content-type", "application/x-www-form-urlencoded; charset=UTF-8")
		req.Header.Add("cookie", cookie)
		req.Header.Add("origin", "https://pub.alimama.com")
		req.Header.Add("referer", "https://pub.alimama.com/promo/search/index.htm?q=%E5%A5%B3%E8%A3%85&_t=1560682452333&toPage=2&perPageSize=50")
		req.Header.Add("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36")
		req.Header.Add("x-requested-with", "XMLHttpRequest")

		res, err := http.DefaultClient.Do(req)
		if err != nil {
			t.Fatal(err.Error())
		}

		body, err := ioutil.ReadAll(res.Body)
		if err != nil {
			t.Fatal(err.Error())
		}
		fmt.Println(string(body))
		res.Body.Close()

	}

}
