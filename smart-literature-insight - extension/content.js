chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action == 'getTabContent') {
    var tabContent = document.body.innerText;
    sendResponse({ tabContent: tabContent });
  }
});
