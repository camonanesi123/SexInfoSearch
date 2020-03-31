from app.db_mysql import db, Xjj
from sqlalchemy import desc, func, and_


class XjjDao():

    #查找某个区域的小姐姐性息
    def list_all_district(self,district):
        print("开始查询当前区域的小姐姐性息")
        xjjs =Xjj.query.filter(
        Xjj.district.like("%" + district + "%") if district is not None else ""
    ).all()
        print("结束询当前区域的小姐姐性息")
        print("{0}区域内小姐姐数量{1}".format(district,len(xjjs)))
        return xjjs

    #分页查找某个区域的小姐姐性息
    def list_page_district(self,district,page,per_page):
        print("开始查询当前区域的小姐姐性息，第{0}页，每页{1}条数据".format(page,per_page))
        xjjs =Xjj.query.filter(
        Xjj.district.like("%" + district + "%") if district is not None else ""
    ).order_by(Xjj.id.desc()).paginate(page, per_page,error_out=False)
        print("结束询当前区域的小姐姐性息")
        return xjjs

    #bootstrap分页查找某个区域的小姐姐性息
    def list_page_bootstrap(self,district,style,offset,limit):
        print("开始查询当前区域的小姐姐性息，第{0}条开始的{1}条数据".format(offset,limit))
        #先查询当前类型的数据的条目
        total = Xjj.query.filter(
            and_(Xjj.district==district if district is not None else "",
            Xjj.style==style if style is not None else "")).count()
        #再查询从开始到offset的数据条目
        xjjs =Xjj.query.filter(
            and_(Xjj.district==district if district is not None else "",
        Xjj.style==style if style is not None else "")
    ).order_by(Xjj.id.desc()).offset(offset).limit(limit)
        if total>100:
            total = 100
        xjjs.total = total
        print(xjjs)
        print("结束询当前区域的小姐姐性息")
        return xjjs

    #查找小姐姐联系方式
    def get_contact_by_id(self, id):
        print("开始查询id为{0}的小姐姐联系方式".format(id))
        rs = Xjj.query.get(id)
        print("结束查询{0}号小姐姐的联系方式".format(id))
        return rs.contact

    #查看小姐姐详情
    def get_details_by_id(self, id):
        print("开始查询id为{0}的小姐姐详细情况".format(id))
        rs = Xjj.query.get(id)
        print("结束查询{0}号小姐姐的详细情况".format(id))
        return rs

    #获取小姐姐城市列表
    def get_xjj_citys(self):
        print("加载小姐姐城市列表")
        citys = db.session.query(Xjj.district).group_by(Xjj.district).all()
        print("结束查询小姐姐性息")
        return citys

    #TELEGRAM调用接口随机查找 某一类型 谋个区域的小姐姐性息
    def get_rand_xjj_for_tg(self,style,district):
        print("开始为tg用户随机查找一条小姐姐性息")
        rs = Xjj.query.filter(
        Xjj.style.like("%" + style + "%") ,
        Xjj.district.like("%" + district + "%"),
    ).order_by(func.rand()).first()
        print("结束查询小姐姐性息")
        return rs