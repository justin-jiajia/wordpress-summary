from database import (
    create_table,
    get_content_by_id_and_md5,
    get_wordpress_post_content,
    update_content_by_id,
)
from ai import get_summary_from_text
from utils import calculate_md5
from flask import Flask, request


def get_summary(id):
    content = get_wordpress_post_content(id)
    if content is None:
        return None
    md5 = calculate_md5(content)
    cachedsummary = get_content_by_id_and_md5(id, md5)
    if cachedsummary is not None:
        return cachedsummary
    generatedsummary = get_summary_from_text(content)
    update_content_by_id(id, md5, generatedsummary)
    return generatedsummary


create_table()
app = Flask(__name__)


@app.get("/getsummary")
def getsummaryhandler():
    postid_str = request.args.get("id")
    if postid_str is None:
        return "请传入‘id’"
    try:
        postid = int(postid_str)
    except:
        return "请传入数字！"
    summarygot = get_summary(postid)
    if summarygot is None:
        return "出错了！"
    return summarygot
