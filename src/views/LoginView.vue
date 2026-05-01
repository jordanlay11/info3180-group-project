<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            type="email"
            v-model.trim="email"
            placeholder="grace@example.com"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="••••••••"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? 'Hide' : 'Show' }}
            </button>
          </div>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="signup-text">
        Don't have an account?
        <router-link to="/register">Sign up here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false,
      showPassword: false,
      apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:5000'
    };
  },
  methods: {
    async handleLogin() {
      this.error = "";

      if (!this.email) {
        this.error = "Email is required.";
        return;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.email)) {
        this.error = "Please enter a valid email address.";
        return;
      }

      if (!this.password) {
        this.error = "Password is required.";
        return;
      }

      this.loading = true;

      try {
        const response = await fetch(`${this.apiUrl}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (response.status === 200 && data.success) {
          this.$router.push('/dashboard');
        } else {
          this.error = data.error || "Login failed. Please try again.";
        }
      } catch (error) {
        console.error("Error logging in:", error);
        this.error = "An error occurred. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f3e6d8 0%, #a83232 100%);
  padding: 20px;
}

.login-card {
  background: #ffffff;
  width: 100%;
  max-width: 430px;
  padding: 42px 40px 36px;
  border-radius: 12px;
  box-shadow: 0 14px 35px rgba(70, 20, 20, 0.22);
}

h2 {
  text-align: center;
  margin-bottom: 28px;
  color: #a83232;
  font-size: 2rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #3e2b2b;
  font-size: 1rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d9c9bd;
  border-radius: 6px;
  font-size: 1rem;
  background: #fffdfb;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #a83232;
  box-shadow: 0 0 0 3px rgba(168, 50, 50, 0.14);
}

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-right: 72px;
}

.toggle-password {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  color: #a83232;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
}

.toggle-password:hover {
  text-decoration: underline;
}

.error {
  margin: 6px 0 14px;
  color: #b00020;
  font-size: 0.92rem;
}

.login-btn {
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(90deg, #b23a3a 0%, #8f2323 100%);
  color: #ffffff;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.login-btn:hover {
  transform: translateY(-1px);
  opacity: 0.96;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.signup-text {
  margin-top: 18px;
  text-align: center;
  font-size: 0.96rem;
  color: #4a3a33;
}

.signup-text a {
  color: #a83232;
  font-weight: 600;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 24px;
  }

  h2 {
    font-size: 1.75rem;
  }
}
</style>