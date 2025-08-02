// ポップアップを開閉する処理

// DOM操作読み込み ページのHTMLが完全に読み込まれた後に以下関数を実行せよ
document.addEventListener("DOMContentLoaded", () => {
  // テンプレート表示用ボタン(id="template_btn")を取得して変数templateBtnに代入
  const templateBtn = document.getElementById("template_btn");
  // (id="template_popup")を取得し、変数template_popupに代入
  const templatePopup = document.getElementById("template_popup");
  // close_btnクラスを取得 closeBtnに代入 querySelectorはCSS風指定
  const closeBtn = document.querySelector(".close_btn");
  // template_textクラスを持つ全ての要素を取得してtemplateTextsに代入
  const templateTexts = document.querySelectorAll(".template_text");
  // メッセージ入力欄(send_message)を取得してmessageInputに代入
  const messageInput = document.getElementById("send_message");

  // 定型文ボタン(templateBtn)をクリックしたらポップアップウィンドウ(templatePopup)をdisplay:blockで表示
  templateBtn.addEventListener("click", () => {
    templatePopup.style.display = "block";
  });

  // ✕ボタンをクリックしたらポップアップウィンドウを非表示(display:none)にする
  closeBtn.addEventListener("click", () => {
    templatePopup.style.display = "none";
  });

  // すべてのtemplate_textに対してクリックされたらその中の文をmessageInputに挿入しポップアップを閉じる

  // querySelectorAll() で取得した templateTexts は NodeList（複数要素）。これは直接 addEventListener() を使えない。forEachを使う
  templateTexts.forEach((el) => {
    el.addEventListener('click', () => {
      messageInput.value = el.textContent;
      templatePopup.style.display = 'none';
    });
  });

});