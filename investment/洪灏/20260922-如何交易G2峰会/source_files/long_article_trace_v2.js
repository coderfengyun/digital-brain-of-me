const traceImg = document.createElement('img')
const url = `${window.location.protocol}//data.card.weibo.com/m/aj/stat`

function submit (value) {
  let id = window.location.href.match(/id=([^?]+)/)

  if (id && (id = id[1])) {
    const ua = encodeURIComponent(window.navigator.userAgent)
    const appkey = ~window.location.search.indexOf('_wb_article_browser_=1')
      ? '2523651897'
      : '3417168152'
    const search = encodeURIComponent(
      window.location.search ? window.location.search.slice(1) : ''
    )
    const to_url = `${url}?id=${id}&appkey=${appkey}&ua=${ua}&${value}&search=${search}&_r=${new Date().getTime()}_${Math.floor(
      Math.random() * 1000
    )}`
    /**
     * sendBeacon 文档
     * https://developer.mozilla.org/zh-CN/docs/Web/API/Navigator/sendBeacon
     */
    if (navigator.sendBeacon) {
      navigator.sendBeacon(to_url)
    } else {
      traceImg.src = to_url
    }
  }
}

function setDomTrack () {
  function report (node) {
    // 曝光插码点 曝光插码点 曝光插码点 曝光插码点 曝光插码点 曝光插码点 曝光插码点 曝光插码点 曝光插码点
    var nodeInfo = node.querySelectorAll('.W_autocut.S_txt1')[0]
    var traceId = nodeInfo.href.match(/id=([^?]+)/)[1].split('#')[0]
    var reason = nodeInfo.getAttribute('trace')
    var submitInfo = `act_code=6935&ext=area:${recommendList[traceId]}:${traceId}:${window.experiment_code}:${reason}`
    submit(submitInfo)
    intersectionObserver.unobserve(node)
  }

  var intersectionObserver = new window.IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.intersectionRatio > 0) {
        report(entry.target)
      }
    })
  })
  var nodes = document.querySelectorAll('.pt_li.pt_li_1.S_bg2')
  nodes.forEach((node, index) => {
    intersectionObserver.observe(node)
  })

  var recomendDom = document.querySelectorAll('.pt_li.pt_li_1.S_bg2')
  recomendDom.forEach((item, index) => {
    item.addEventListener('click', function (e) {
      // 点击插码点 点击插码点 点击插码点 点击插码点 点击插码点 点击插码点 点击插码点 点击插码点 点击插码点

      var nodeInfo = item.querySelectorAll('.W_autocut.S_txt1')[0]
      var traceId = nodeInfo.href.match(/id=([^?]+)/)[1].split('#')[0]
      var reason = nodeInfo.getAttribute('trace')

      var submitInfo = `act_code=3694&ext=area:text:${index}:${traceId}:${window.experiment_code}:${reason}`
      submit(submitInfo)
    })
  })
}

// var targetNode = document.querySelectorAll('.pt_ul.clearfix')[0];
var targetNode = document.querySelectorAll('[node-type="recommend"]')[0]
// 观察者的选项(要观察哪些突变)
var config = { attributes: true, childList: true, subtree: true }
// 当观察到突变时执行的回调函数
var recommendList = {}
var callback = function (mutationsList) {
  var recomendDomList = document.querySelectorAll('.pt_li.pt_li_1.S_bg2')
  recomendDomList.forEach((item, index) => {
    recommendList[
      item
        .querySelectorAll('.W_autocut.S_txt1')[0]
        .href.match(/id=([^?]+)/)[1]
        .split('#')[0]
    ] = index
  })

  setDomTrack()
}
// 创建一个链接到回调函数的观察者实例
var observer = new window.MutationObserver(callback)
// 开始观察已配置突变的目标节点
observer.observe(targetNode, config)
