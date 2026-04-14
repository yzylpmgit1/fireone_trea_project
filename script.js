// 平滑滚动功能：实现导航链接点击后平滑滚动到对应区域
// 选择所有以#开头的链接
// 为每个链接添加点击事件监听器
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault(); // 阻止默认的跳转行为
        // 平滑滚动到目标元素
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth' // 使用平滑滚动效果
        });
    });
});

// 导航栏滚动效果：根据滚动位置调整导航栏样式
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) { // 当滚动超过100px时
        navbar.style.background = 'rgba(255, 255, 255, 0.98)'; // 增加背景透明度
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)'; // 增加阴影效果
    } else { // 当滚动小于100px时
        navbar.style.background = 'rgba(255, 255, 255, 0.95)'; // 恢复默认背景透明度
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)'; // 恢复默认阴影效果
    }
});

// 表单验证：确保联系表单的必填字段都已填写
const contactForm = document.querySelector('.contact-form form');
if (contactForm) { // 检查表单是否存在
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault(); // 阻止表单默认提交行为
        // 获取表单字段值
        const name = this.querySelector('input[type="text"]').value;
        const email = this.querySelector('input[type="email"]').value;
        const message = this.querySelector('textarea').value;
        
        // 验证字段是否为空
        if (!name || !email || !message) {
            alert('请填写所有必填字段'); // 提示用户填写所有字段
            return; // 停止执行后续代码
        }
        
        // 模拟表单提交成功
        alert('表单提交成功！我们会尽快与您联系。');
        this.reset(); // 重置表单
    });
}

// 功能卡片动画：当卡片进入视口时显示动画效果
const featureCards = document.querySelectorAll('.feature-card');
// 创建交叉观察器，用于检测元素是否进入视口
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) { // 当元素进入视口时
            entry.target.style.opacity = '1'; // 设置透明度为1
            entry.target.style.transform = 'translateY(0)'; // 恢复原始位置
        }
    });
}, { threshold: 0.1 }); // 当元素10%进入视口时触发

// 为每个功能卡片设置初始样式并开始观察
featureCards.forEach(card => {
    card.style.opacity = '0'; // 初始透明度为0
    card.style.transform = 'translateY(50px)'; // 初始位置向下偏移50px
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease'; // 过渡效果
    observer.observe(card); // 开始观察元素
});

// 应用卡片动画：与功能卡片类似
const appCards = document.querySelectorAll('.app-card');
appCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(50px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// 优势项动画：与功能卡片类似
const benefitItems = document.querySelectorAll('.benefit-item');
benefitItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(50px)';
    item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(item);
});

// 英雄区域打字效果：实现文字逐个显示的动画
const heroText = document.querySelector('.hero-content h1');
if (heroText) { // 检查元素是否存在
    const text = heroText.textContent; // 获取原始文本内容
    heroText.textContent = ''; // 清空文本
    let i = 0; // 初始化计数器
    const typeWriter = () => {
        if (i < text.length) { // 当计数器小于文本长度时
            heroText.textContent += text.charAt(i); // 添加当前字符
            i++; // 计数器加1
            setTimeout(typeWriter, 100); // 100毫秒后继续执行
        }
    };
    typeWriter(); // 开始执行打字动画
}