<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Register</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="fname">First Name</label>
          <input
            id="fname"
            type="text"
            v-model="formData.fname"
            placeholder="Amy"
            required
          />
        </div>

        <div class="form-group">
          <label for="lname">Last Name</label>
          <input
            id="lname"
            type="text"
            v-model="formData.lname"
            placeholder="Rose"
            required
          />
        </div>

        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            type="text"
            v-model="formData.username"
            placeholder="amyrose"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            type="email"
            v-model="formData.email"
            placeholder="amy@example.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              v-model="formData.password"
              placeholder="••••••••"
              required
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

        <div class="form-group">
          <label for="gender">Gender</label>
          <select id="gender" v-model="formData.gender" required>
            <option value="" disabled>Select your gender</option>
            <option value="m">Male</option>
            <option value="f">Female</option>
            <option value="o">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label for="date_of_birth">Date of Birth</label>
          <input
            id="date_of_birth"
            type="date"
            v-model="formData.date_of_birth"
            required
          />
        </div>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <p class="signup-text">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterView",
  data() {
    return {
      formData: {
        fname: "",
        lname: "",
        username: "",
        email: "",
        password: "",
        gender: "",
        date_of_birth: ""
      },
      error: "",
      successMessage: "",
      loading: false,
      showPassword: false
    };
  },
  methods: {
    async handleRegister() {
      // Reset messages
      this.error = "";
      this.successMessage = "";

      // Validate email
      if (!this.formData.email) {
        this.error = "Email is required.";
        return;
      }

      // Validate email format
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.formData.email)) {
        this.error = "Please enter a valid email address.";
        return;
      }

      // Validate password
      if (!this.formData.password) {
        this.error = "Password is required.";
        return;
      }

      if (this.formData.password.length < 6) {
        this.error = "Password must be at least 6 characters.";
        return;
      }

      
      if (!this.formData.fname || !this.formData.lname || !this.formData.username || !this.formData.gender || !this.formData.date_of_birth) {
        this.error = "Please fill in all fields.";
        return;
      }

      this.loading = true;

      
      try {
        const response = await fetch('/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData)
        });

        const data = await response.json();

        if (response.status === 201 || data.message || data.success) {
          this.successMessage = "Registration successful! Redirecting to login...";
          
          // Clear form
          this.formData = {
            fname: "",
            lname: "",
            username: "",
            email: "",
            password: "",
            gender: "",
            date_of_birth: ""
          };
          
          // Redirect to login after 2 seconds
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        } else {
          this.error = data.error || "Registration failed. Please try again.";
        }
      } catch (error) {
        console.error("Error registering user:", error);
        this.error = "An error occurred while registering. Please try again.";
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

input, select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d9c9bd;
  border-radius: 6px;
  font-size: 1rem;
  background: #fffdfb;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

input:focus, select:focus {
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

.success {
  margin: 6px 0 14px;
  color: #2e7d32;
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