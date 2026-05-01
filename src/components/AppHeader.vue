<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">VueJS with Flask</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/favorites">Favorites</RouterLink>
            </li>
            <li class="nav-item">
              <button @click="handleLogout" class="nav-link" style="background: none; border: none; cursor: pointer;">Logout</button>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";

const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const handleLogout = async () => {
  try {
    await fetch(`${apiUrl}/logout`, {
      method: 'POST',
      credentials: 'include'
    })
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    
    router.push('/login')
  }
}
</script>

<style>
/* Add any component specific styles here */
</style>