window.pjaxLoaded = getanddisplay
window.onload = getanddisplay

function getanddisplay() {
  const currentUrl = window.location.href;
  const url = new URL(currentUrl);
  const pValue = url.searchParams.get('p');
  if (pValue != null) {
    const newDiv = document.createElement('div');
    newDiv.style.border = '2px solid blue';
    const targetDiv = document.getElementById('post_content');
    if (targetDiv) {
      targetDiv.parentNode.insertBefore(newDiv, targetDiv);
      fetch("https://summary.hijiajia.top/getsummary?id=" + pValue)
        .then((res) => {
          if (!res.ok) {
            newDiv.innerText = "出错了"
            console.log(res.body)
            throw new Error(res)
          }
          return res
        }).then(res => res.text()).then(res => {
          targetDiv.className = "type_blink"
          let index = 0
          function writing() {
            if (index < res.length) {
              newDiv.innerHTML += res[index++]
              requestAnimationFrame(writing)
            } else {
              targetDiv.className = ""
            }
          }
          writing()
        })
    } else {
      console.error('未找到指定 ID 的 div');
    }
  }
}