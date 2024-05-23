<template>
  <div class="container-fluid d-flex flex-column min-vh-100 p-0" style="background-color: #FFF9DB;">
    <header class="mb-4">
      <div class="wrapper">
        <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #FFF2B2;">
          <div class="container-fluid d-flex justify-content-between align-items-center">
            <img alt="Vue logo" src="@/assets/Duck9_logo.png" width="100" height="100" @click="goToHome"/>
            <span class="navbar-title" @click="goToHome">
              <span class="duck">덕</span>친을 <span class="nine">9</span>해요
            </span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                  <li class="nav-item">
                    <RouterLink :to="{ name: 'home'}" class="nav-link">Duck9 홈</RouterLink>
                  </li>
                  <li class="nav-item" v-show="!store.isLogin">
                    <RouterLink :to="{ name: 'signup'}" class="nav-link">회원가입</RouterLink>
                  </li>
                  <li class="nav-item" v-show="!store.isLogin">
                    <RouterLink :to="{ name: 'login'}" class="nav-link">로그인</RouterLink>
                  </li>
                  <li class="nav-item" v-show="store.isLogin">
                    <RouterLink :to="{ name: 'joined'}" class="nav-link">내 둥지들</RouterLink>
                  </li>
                  <li class="nav-item me-3" v-show="store.isLogin">
                    <a href="" @click.prevent="logOut" class="nav-link">로그아웃</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </header>
    <!-- <main class="flex-grow-1 d-flex justify-content-center align-items-center"> -->
    <main>
      <RouterView />
    </main>
    <footer class="footer-sticky mt-auto py-3 text-center">
      <div>
        <p class="mb-0 footer-text">제작사: 김도영 공식 팬클럽</p>
        <img alt="Vue logo" src="@/assets/project_logo.png" width="30" height="20" />
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router';

const store = useMovieStore()

const router = useRouter()

const logOut = () => {
  store.logOut()
}

const goToHome = function () {
  router.push({ name: 'home' })
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

.footer-sticky {
  box-shadow: 0 -2px 5px rgba(83, 55, 13, 0.1);
  background: #fdf3c1;
  background: #fdf3c1;
}

.navbar {
  font-family: 'Gowun Dodum', sans-serif;
  font-size: 1.2rem;
}

.navbar-title {
  font-family: 'Gowun Dodum', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FF8C00;
  background: #fcf7f0;
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.duck, .nine {
  font-weight: bolder;
  font-size: 2rem;
  color: #242424; /* 덕과 9의 색상 변경 */
}

.nav-link, .navbar-brand {
  color: #ff7300 !important;
}

body {
  background-color: #FFF9DB;
  font-family: 'Gowun Dodum', sans-serif;
  margin: 0;
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.footer-text {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 13px;
}

footer p {
  margin: 0;
}

.navbar-nav .nav-item {
  margin-right: 1rem;
}

.navbar-nav .nav-item:last-child {
  margin-right: 0;
}

@media (max-width: 991.98px) {
  .collapse:not(.show) {
    display: none;
  }
  .collapse.show {
    display: block;
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #FFF2B2;
    width: 100%;
    z-index: 1;
  }
  .navbar-nav {
    flex-direction: column;
    align-items: flex-end;
    width: 100%;
  }
  .nav-item {
    width: 100%;
    text-align: right;
  }
}
</style>