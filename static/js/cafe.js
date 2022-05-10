$(document).ready(showCafeDetail);
function showCafeDetail(){
    let id = new URLSearchParams(location.search).get('id');
    $.ajax({
        type:'GET',
        url:'/api/cafe/detail/'+id,
        success:(response)=>{
            let cafe_id = response['cafes']['cafe_id'];
            let cafe_name = response['cafes']['cafe_name'];
            let cafe_info = response['cafes']['cafe_detail_info'];
            let address = response['cafes']['address'];
            let cafe_image = response['cafes']['cafe_image'];
            // let reviews = response['reviews'];
            let x = response['cafes']['cafe_x'];
            let y = response['cafes']['cafe_y'];
            let cafe_notice = response['cafes']['cafe_notice'];
            $('#cafe-name').text(cafe_name);
            $('#info').text(cafe_info);
            $('#notice').text(cafe_notice);
            kakaoMapAPI(x,y);
        }

    })
}

function kakaoMapAPI(x, y) {
    let container = document.getElementById('map');
    let options = { //지도를 생성할 때 필요한 기본 옵션
        center: new kakao.maps.LatLng(x, y), //지도의 중심좌표.
        level: 3 //지도의 레벨(확대, 축소 정도)
    };
    let map = new kakao.maps.Map(container, options);
}

