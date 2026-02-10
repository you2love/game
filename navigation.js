// 自动定位到当前页的导航项
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-tree a');
    
    navLinks.forEach(function(link) {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPage) {
            // 移除所有active类
            document.querySelectorAll('.nav-tree li').forEach(function(li) {
                li.classList.remove('active');
            });
            
            // 添加active类到当前项
            link.parentElement.classList.add('active');
            
            // 滚动到当前项并居中
            const sidebar = document.querySelector('.sidebar');
            const activeLink = link;
            
            setTimeout(function() {
                const sidebarRect = sidebar.getBoundingClientRect();
                const linkRect = activeLink.getBoundingClientRect();
                
                const offsetTop = linkRect.top - sidebarRect.top - (sidebarRect.height / 2) + (linkRect.height / 2);
                
                sidebar.scrollTo({
                    top: sidebar.scrollTop + offsetTop,
                    behavior: 'smooth'
                });
            }, 100);
        }
    });

    // 导航栏折叠功能
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            sidebar.classList.toggle('open');
            sidebarToggle.classList.toggle('active');
            mainContent.classList.toggle('expanded');
        });
    }

    // 点击导航项后，在小屏幕上自动关闭侧边栏
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('open');
                sidebar.classList.add('collapsed');
                sidebarToggle.classList.remove('active');
                mainContent.classList.add('expanded');
            }
        });
    });
});