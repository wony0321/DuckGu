<template>
  <main class="login-container d-flex justify-content-center align-items-center">
    <div class="login-box">
      <h2 class="login-title">🐣로그인 페이지입니덕🐣</h2>
      <form @submit.prevent="logIn" class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">아이디가 뭡니꽉?</label>
          <input type="text" v-model.trim="username" id="username" class="form-input" autocomplete="username">
        </div>
        <div class="form-group">
          <label for="password" class="form-label">비밀번호 486:</label>
          <input type="password" v-model.trim="password" id="password" class="form-input" autocomplete="current-password">
        </div>
        <input type="submit" class="form-submit" value="로그인">
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

const username = ref(null)
const password = ref(null)

const store = useMovieStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  background-color: #FFF9DB; 
  font-family: 'Gowun Dodum', sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.login-box {
  font-family: 'Gowun Dodum', sans-serif;
  width: 90%;
  max-width: 400px;
  text-align: center;
  background: #FFF2B2;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-title {
  color: #141414;
  font-size: 1.8rem;
  font-family: 'Nanum Gothic', sans-serif;
  margin-bottom: 20px;
  text-align: center;
}

.login-form {
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
  color: #FF7300;
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
