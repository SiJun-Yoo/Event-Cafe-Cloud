function login() {
    let user_id = $('#input-userId').val()
    let user_pw = $('#input-userPw').val()

    if (user_id == "") {
        $('#help-id-login').text("아이디를 입력하세요")
        $('#input-userId').focus()
        return
    } else {
        $('#help-id-login').text("")
    }

    if (user_pw == "") {
        $('#help-pw-login').text("비밀번호를 입력하세요")
        $('#input-userPw').focus()
        return
    } else {
        $('#help-pw-login').text("")
    }

    $.ajax({
        type: "POST",
        url: "/auth/token_login",
        data: {
            user_id_give: $('#input-userId').val(),
            user_pw_give: $('#input-userPw').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('jwt_token', response['token'], {path: '/'});
                alert('로그인 되었습니다!')
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}

function logout() {
    $.removeCookie('jwt_token', {path: '/'})
    alert('로그아웃!')
    window.location.href = "/"
}