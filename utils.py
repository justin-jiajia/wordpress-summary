import re
import hashlib

calculate_md5 = lambda text: hashlib.md5(text.encode()).hexdigest()
remove_html_tags = lambda text: re.sub(r"<.*?>", "", text)
