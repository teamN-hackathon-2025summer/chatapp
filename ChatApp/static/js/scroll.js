document.addEventListener("DOMContentLoaded", () => {
  // 画像などで高さがあとから伸びても追従
  const toBottom = () =>
    // ページ全体のスクロール位置を最下部へ
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "auto" });

  toBottom();

});
