<template>
  <main class="create-meet-container">
    <h1 class="create-meet-title">둥지 생성하기</h1>
    <form @submit.prevent="handleCreateMeet" class="create-meet-form">
      <div class="form-group">
        <label for="name" class="form-label">둥지 이름 머할꽉?</label>
        <input type="text" id="name" v-model="name" class="form-input" />
      </div>

      <div class="form-group">
        <label for="genre" class="form-label">좋아하는 장르를 선택할꽉? (여러 개 가능)</label>
        <select id="genre" multiple class="form-input">
          <option
            v-for="genre in [...new Set(keywords.map(keyword => keyword.genre).filter(genre => genre))]"
            :key="genre"
            :value="genre"
            :class="{ selected: selectedGenres.includes(genre)}"
            @click="toggleSelection(selectedGenres, genre)"
          >
            {{ genre }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="origin_country" class="form-label">좋아하는 국가를 선택할꽉? (여러 개 가능)</label>
        <select id="origin_country" multiple class="form-input">
          <option
            v-for="country in [...new Set(keywords.map(keyword => keyword.origin_country).filter(country => country))]"
            :key="country"
            :value="country"
            :class="{ selected: selectedCountries.includes(country) }"
            @click="toggleSelection(selectedCountries, country)"
          >
            {{ country }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="era" class="form-label">좋아하는 시대를 선택할꽉? (여러 개 가능)</label>
        <select id="era" multiple class="form-input">
          <option
            v-for="era in [...new Set(keywords.map(keyword => keyword.era).filter(era => era))]"
            :key="era"
            :value="era"
            :class="{ selected: selectedEras.includes(era) }"
            @click="toggleSelection(selectedEras, era)"
          >
            {{ era }}
          </option>
        </select>
      </div>
      
      <input type="submit" class="form-submit" value="Create Group">
    </form>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()

const name = ref('')
const user = ref(store.user)
const keywords = ref(store.keywords)
const selectedGenres = ref([])
const selectedCountries = ref([])
const selectedEras = ref([])

const toggleSelection = (selectedList, value) => {
  const index = selectedList.indexOf(value)
  if (index === -1) {
    selectedList.push(value)
  } else {
    selectedList.splice(index, 1)
  }
}

const handleCreateMeet = function () {
  const selectedKeywords = keywords.value.filter(keyword => 
    selectedGenres.value.includes(keyword.genre) || 
    selectedCountries.value.includes(keyword.origin_country) || 
    selectedEras.value.includes(keyword.era)
  ).map(keyword => keyword.id)

  const payload = {
    name: name.value,
    keywords: selectedKeywords,
    users: [user.value.id]
  }

  store.createMeet(payload)
}


</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  background-color: #FFF9DB; /* 연한 노란색 배경 */
  font-family: 'Gowun Dodum', sans-serif; /* 기본 본문 글꼴 */
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.create-meet-container {
  width: 90%;
  max-width: 500px;
  text-align: center;
  background: #FFF2B2; /* 연한 주황색 배경 */
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
}

.create-meet-title {
  font-family: 'Nanum Gothic', sans-serif; /* 제목 글꼴 */
  color: #FF8C00; /* 주황색 텍스트 */
  font-size: 2rem;
  margin-bottom: 20px;
  text-align: center;
}

.create-meet-form {
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
  color: #131313; /* 주황색 텍스트 */
  text-align: center;
  font-family: 'Gowun Dodum', sans-serif;

}

.form-input, select, option {
  font-family: 'Gowun Dodum', sans-serif; /* 입력 필드 및 선택 요소 글꼴 */
  width: 100%;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #FF8C00;
  font-size: 1rem;
}

option {
  border: none;
}

.form-submit {
  font-family: 'Gowun Dodum', sans-serif;
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

option.selected {
  background-color: rgb(255, 236, 175);
  background-color: rgb(255, 236, 175);
}
</style>
