<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Register</h2>

      <form @submit.prevent="handleRegister" id="registerForm">
        <div class="form-group">
            <label for="fname">First Name</label>
            <input
                id="name"
                type="text"
                v-model.trim="name"
                placeholder="Amy"
            />
        </div>

        <div class="form-group">
            <label for="lname">Last Name</label>
            <input
                id="name"
                type="text"
                v-model.trim="name"
                placeholder="Rose"
            />
        </div>
        <div class="form-group">
            <label for="username">Username</label>
            <input
                id="username"
                type="text"
                v-model.trim="username"
                placeholder="amyrose"
            />
        </div>

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

        <div class="form-group">
            <label for="gender">Gender</label>
            <select id="gender" v-model="gender">
                <option value="" disabled>Select your gender</option>
                <option value="m">Male</option>
                <option value="f">Female</option>
                <option value="o">Other</option>
            </select>
        </div>

        <div class="form-group">
            <label for="age">Age</label>
            <input
                id="age"
                type="number"
                v-model.trim="age"
                placeholder="25"
            />
        </div>

         <div class="form-group">
            <label for="date_of_birth">Date of Birth</label>
            <input
                id="date_of_birth"
                type="date"
                v-model.trim="date_of_birth"
            />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? 'Registering...' : 'Registered' }}
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
    import { ref, onMounted } from 'vue';
    const csrf_token = ref('');

    const successMessage = ref('');

    const errorMessage = ref([]);

    const formData = ref({
        fname: '',
        lname: '',
        username: '',
        Email: '',
        password: '',
        age: '',
        gender: '',
        date_of_birth: '',
    });
    
    /*
    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                csrf_token.value = data.csrf_token;
            })
            .catch(error => {
            console.error('Error fetching CSRF token:', error);
            });
    }

    onMounted(() => {
        getCsrfToken();
    });

    
    function handleRegister() {
        let registerForm = document.getElementById('registerForm');
        let form_data = new FormData(registerFormForm);
        errorMessage.value = [];
        successMessage.value = '';

        fetch('/api/v1/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token.value
            },
            body: JSON.stringify(formData.value)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                successMessage.value = data.message;
                formData.value = {
                    fname: '',
                    lname: '',
                    username: '',
                    Email: '',
                    password: '',
                    gender: '',
                    age: '',
                    date_of_birth: ''
                };
            } else {
                errorMessage.value = data.message;
            }
        })
        .catch(error => {
            console.error('Error registering user:', error);
            errorMessage.value = 'An error occurred while registering. Please try again.';
        });
    }*/

 
    export default {
        name: "RegisterView",
        data() {
            return {
            email: "",
            password: "",
            error: "",
            loading: false,
            showPassword: false
            };
        },
        methods: {
            handleRegister() {
                this.error = "";
                let registerForm = document.getElementById('registerForm');
                let form_data = new FormData(registerFormForm);
                errorMessage.value = [];
                successMessage.value = '';



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

                fetch('/api/v1/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token.value
                    },
                    body: JSON.stringify(formData.value)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successMessage.value = data.message;
                        formData.value = {
                            fname: '',
                            lname: '',
                            username: '',
                            Email: '',
                            password: '',
                            gender: '',
                            age: '',
                            date_of_birth: ''
                        };
                    } else {
                        errorMessage.value = data.message;
                    }
                })
                .catch(error => {
                    console.error('Error registering user:', error);
                    errorMessage.value = 'An error occurred while registering. Please try again.';
                });
                /*
                // Temporary demo login
                setTimeout(() => {
                    this.loading = false;
                    alert("Login successful.");
                    this.$router.push("/");
                }, 1000);*/
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