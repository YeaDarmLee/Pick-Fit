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
function kakaoShare(){   
  Kakao.Link.sendDefault({
      objectType: 'feed',
      content: {
      title: '오늘의 디저트',
      description: '아메리카노, 빵, 케익',
      imageUrl:
          'http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg',
      link: {
          mobileWebUrl: 'https://developers.kakao.com',
          androidExecutionParams: 'test',
      },
      },
      itemContent: {
      profileText: 'Kakao',
      profileImageUrl: 'http://mud-kage.kakao.co.kr/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png',
      titleImageUrl: 'http://mud-kage.kakao.co.kr/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png',
      titleImageText: 'Cheese cake',
      titleImageCategory: 'Cake',
      items: [
          {
          item: 'Cake1',
          itemOp: '1000원',
          },
          {
          item: 'Cake2',
          itemOp: '2000원',
          },
          {
          item: 'Cake3',
          itemOp: '3000원',
          },
          {
          item: 'Cake4',
          itemOp: '4000원',
          },
          {
          item: 'Cake5',
          itemOp: '5000원',
          },
      ],
      sum: '총 결제금액',
      sumOp: '15000원',
      },
      social: {
      likeCount: 10,
      commentCount: 20,
      sharedCount: 30,
      },
      buttons: [
      {
          title: '웹으로 이동',
          link: {
          mobileWebUrl: 'https://developers.kakao.com',
          },
      },
      ]
  });
} 