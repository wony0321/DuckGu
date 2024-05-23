<template>
  <main class="signup-container d-flex justify-content-center align-items-center">
    <div class="signup-box">
      <h2 class="signup-title">🐣회원가입 페이지입니덕🐣</h2>
      <form @submit.prevent="signUp" class="signup-form">
        <div class="form-group">
          <label for="username" class="form-label">아이디는 뭐로 하실겁니꽉?</label>
          <input type="text" v-model.trim="username" id="username" class="form-input">
        </div>
        <div class="form-group">
          <label for="email" class="form-label">이메일을 알려주실 수 있으십니꽉?</label>
          <input type="email" v-model.trim="email" id="email" class="form-input">
        </div>
        <div class="form-group">
          <label for="password1" class="form-label">비밀번호는 뭐로 하실겁니꽉?</label>
          <input type="password" v-model.trim="password1" id="password1" class="form-input">
        </div>
        <div class="form-group">
          <label for="password2" class="form-label">비밀번호를 한 번 더 입력해줄 수 있을꽉?</label>
          <input type="password" v-model.trim="password2" id="password2" class="form-input">
        </div>
        <input type="submit" class="form-submit" value="회원가입">
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

const username = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useMovieStore()

const signUp = function () {
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  background-color: #FFF9DB; /* 연한 노란색 배경 */
  font-family: 'Gowun Dodum', sans-serif; /* 귀여운 글꼴 */
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.signup-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.signup-box {
  font-family: 'Gowun Dodum', sans-serif;
  width: 90%;
  max-width: 400px;
  text-align: center;
  background: #FFF2B2; /* 연한 주황색 배경 */
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.signup-title {
  color: #141414; /* 주황색 텍스트 */
  font-size: 1.8rem; /* 변경된 글씨 크기 */
  font-family: 'Nanum Gothic', sans-serif; /* 제목 글씨체 */
  margin-bottom: 20px;
  text-align: center;
}

.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-label {
  margin-bottom: 5px;
  color: #FF7300; /* 주황색 텍스트 */
  text-align: center;
}

.form-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #FF8C00;
  font-size: 1rem;
}

.form-submit {
  background-color: #FF8C00;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 15px;
}

.form-submit:hover {
  background-color: #FF7300;
}
</style>