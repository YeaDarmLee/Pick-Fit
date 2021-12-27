/*!
* Start Bootstrap - Agency v7.0.6 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector('#mainNav');
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove('navbar-shrink')
    } else {
      navbarCollapsible.classList.add('navbar-shrink')
    }

  };

  // Shrink the navbar 
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector('#mainNav');
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: '#mainNav',
      offset: 74,
    });
  };

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector('.navbar-toggler');
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll('#navbarResponsive .nav-link')
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener('click', () => {
      if (window.getComputedStyle(navbarToggler).display !== 'none') {
        navbarToggler.click();
      }
    });
  });

});


/*
** alert 함수 **
state = 상태 icon = "warning" "error" "success" "info"
비동기 처리 위해 funType, url 받아와 사용
*/
function alertStart(state, title, message, funType, text, time) {
  Swal.fire({
    icon: state,
    title: title,
    text: message,
  }).then(function(){
    if (funType == 'replace') {
      change_url(text, time)
    } else if (funType == 'click') {
      $(text).click()
    } else if (funType == 'reload') {
      location.reload()
    }
  });
};

function change_url(url, time) {
  $('#load').slideToggle()
  setTimeout(function () {
    location.replace(url)
  }, time);
}

function goRecommend() {
  change_url('/recommend',1000)
}

function goUrl(url) {
  if (url) {
    window.open(url)
  }
}

//kakao share
function kakaoClotheShare(gender, style){

  const f_content = document.getElementById("f_content").textContent.replace(" | ","").replace("얼굴형 : ","")
  const s_content = document.getElementById("s_content").textContent.replace("체형 : ","")
  const fd_content = document.getElementById("fd_content").textContent
  const sd_content = document.getElementById("sd_content").textContent

  let styledata = '';
  // 남자 여자 별로 스타일 달라서 남자여자도 구분해서 스타일 이름하고 이미지 경로 지정해줘야함
  if (gender == 1) {
    switch(style) {
      case '1':
        styledata = '로맨틱'
        break;
      case '2':
        styledata = '모던'
        break;
      case '5':
        styledata = '스트리트'
        break;
      case '3':
        styledata = '스포티'
        break;
      case '4':
        styledata = '클래식'
        break;
    }
  } else {
      switch(style) {
        case '6':
          styledata = '캐주얼'
          break;
        case '2':
          styledata = '모던'
          break;
        case '5':
          styledata = '스트리트'
          break;
        case '7':
          styledata = '밀리터리'
          break;
        case '3':
          styledata = '스포티'
          break;
    }
  }

  console.log(styledata)
  
  Kakao.Link.sendCustom({
    templateId: 67577,
    templateArgs: {
      'title': f_content + s_content,
      'description': fd_content + sd_content,
      'style': styledata,
    }
  });
} 

//kakao share
function kakaoCodyShare(userNm,c_outerData,topData,bottomData){
  let outerFile = new File([c_outerData], {
    type: "application/jpg"
  });
  
  let topFile = new File([topData], {
    type: "application/jpg"
  });
  
  let bottomFile = new File([bottomData], {
    type: "application/jpg"
  });

  console.log(outerFile)
  console.log(topFile)
  console.log(bottomFile)

  // 파일 이미지 업로드로 카카오 url 받은 후 해당 url 파싱

  Kakao.Link.uploadImage({
    file: topFile
  }).then(function(res){
    console.log(res.infos.original.url)
    // document.getElementById('uploadUrl').value = res.infos.original.url;
  });
  
  Kakao.Link.sendCustom({
    templateId: 67579,
    templateArgs: {
      'userNm': userNm,
      'img1':'',
      'img2':'',
      'img3':''
    }
  });
} 