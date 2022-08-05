import Vue from 'vue'
/**
 * author: zuokun
 * 水印
 * text：水印文字
 * font：字体
 * textColor：文字颜色
 * width：宽度
 * height：高度
 * textRotate：偏转度 -90到0， 负数值，不包含-90
 */
Vue.directive('watermark', (el, binding) => {
	let text = binding.value.text;
	let font = binding.value.font || "15px Microsoft JhengHei";
	let textColor = binding.value.textColor || "rgba(215, 215, 215, 0.2)";
	let width = binding.value.width || 150;
	let height = binding.value.height || 150;
	let textRotate = binding.value.textRotate || -30;

	function addWaterMarker(parentNode) {
		var can = document.createElement('canvas');
		parentNode.appendChild(can);
		can.width = width;
		can.height = height;
		can.style.display = 'none';
		var cans = can.getContext('2d');
		cans.rotate(textRotate * Math.PI / 180);
		cans.font = font;
		cans.fillStyle = textColor;
		cans.textAlign = 'left';
		cans.textBaseline = 'Middle';
		cans.fillText(text, 0, can.height);
		parentNode.style.backgroundImage = "url(" + can.toDataURL("image/png") + ")";
	}
	addWaterMarker(el)
})
