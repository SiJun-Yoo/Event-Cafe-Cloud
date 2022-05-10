import jwt
import requests as requests
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from controller.auth_controller import SECRET_KEY
from database import DB
from ectoekn import ECTOKEN

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/profile')
def home():
    user = ECTOKEN.get_token(object)
    if user is not None:
        if user["cafe"] >= 1:
            my_cafe = DB.find_one("cafes", {'user_id': user["user_id"]}, {'_id': False})
            return render_template('userProfile.html', user=user, my_cafe=my_cafe)
        else:
            return render_template('userProfile.html', user=user)
    else:
        return render_template('userProfile.html', msg="로그인 정보가 없습니다")


@bp.route('/cafe/manage/<cafe_idx>')
def cafe_manage(cafe_idx):
    user = ECTOKEN.get_token(object)
    if user is None:
        return render_template('index.html')
    else:
        return render_template('cafeManagement.html', user=user, cafe_idx=cafe_idx)


@bp.route('/cafe/register')
def cafe_register_form():
    user = ECTOKEN.get_token(object)
    if user is None:
        return render_template('index.html')
    else:
        return render_template('cafeRegister.html', user=user)


@bp.route('api/cafe/management', methods=["GET"])
def show_cafe_manage():
    ###############################
    #todo 이벤트 DB 생성후, 추가 예정#
    ###############################
    return


@bp.route('/api/cafe/register', methods=["POST"])
def cafe_register():
    user_id = ECTOKEN.get_user_id(object)
    cafe_name = request.form['cafe_name_give']
    cafe_short_info = request.form['cafe_short_info_give']
    cafe_detail_info = request.form['cafe_info_give']
    cafe_notice = request.form['cafe_notice_give']
    cafe_image = request.files['cafe_image_give']
    cafe_zipcode = request.form['cafe_zipcode_give']
    cafe_address = request.form['cafe_address_give']
    cafe_address_detail = request.form['cafe_address_detail']
    cafe_count = DB.count_collection("cafes")
    extension = cafe_image.filename.split('.')[-1]

    save_to = f'static/cafe_pics/{user_id}_{cafe_name}.{extension}'
    cafe_image.save(save_to)

    if cafe_count == 0:
        max_value = 1
    else:
        max_value = DB.idx_plus("cafes")

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "rq6sgwt7kz",
        "X-NCP-APIGW-API-KEY": "TsaTRhEbL4iTC5ne25dprSThp28vxAiHeOOnUEeA"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={cafe_address}",
                     headers=headers)
    response = r.json()

    if response["status"] == "OK":
        x = float(response["addresses"][0]["x"])
        y = float(response["addresses"][0]["y"])

    doc = {
        "idx": max_value,
        "user_id": user_id,
        "cafe_name": cafe_name,
        "cafe_short_info": cafe_short_info,
        "cafe_detail_info": cafe_detail_info,
        "cafe_notice": cafe_notice,
        "cafe_image": f"{user_id}_{cafe_name}.{extension}",
        "cafe_zipcode": cafe_zipcode,
        "cafe_address": cafe_address,
        "cafe_address_detail": cafe_address_detail,
        "cafe_x": x,
        "cafe_y": y
    }

    DB.update_one("users", {'user_id': user_id}, {'$set': {'cafe': 1}})
    DB.insert(collection="cafes", data=doc)
    return jsonify({'result': 'success'})


@bp.route('/api/update', methods=["POST"])
def update():
    user_id = ECTOKEN.get_user_id(object)
    user_nickname = request.form['user_nickname_give']
    user_info = request.form['user_userinfo_give']
    user_profile = request.files['user_profile_give']

    extension = user_profile.filename.split('.')[-1]

    save_to = f'static/profile_pics/{user_id}.{extension}'
    user_profile.save(save_to)

    new_doc = {
        "user_nickname": user_nickname,
        "user_profile": f"{user_id}.{extension}",
        "user_info": user_info,
    }

    DB.update_one("users", {'user_id': user_id}, {'$set': new_doc})
    return jsonify({'result': 'success'})
