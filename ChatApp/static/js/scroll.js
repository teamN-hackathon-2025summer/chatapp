// ページが読み込まれたときと、新しいメッセージが追加されたときに自動スクロールする
document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.querySelector(".chat_messages");

  // 下までスクロールする関数
  const scrollToBottom = () => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  // ページ読み込み時に実行
  scrollToBottom();

  // (オプション) 新しい要素が追加されたときにも実行
  const observer = new MutationObserver(scrollToBottom);
  observer.observe(chatMessages, { childList: true });
});
