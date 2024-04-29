<template>
  <div class="product-detail-container">
    <div class="product-detail">
      <h1>{{ product.name }}</h1>
      <img :src="'/' + product.image_url" alt="Product Image" class="product-image" />
      <p>{{ product.description }}</p>
      <p>Price: ${{ product.price }}</p>
      <p>Discount: {{ product.discount }}%</p>
      <p>Category: {{ product.category }}</p>
      <p>Stock: {{ product.stock_quantity }}</p>
      <p>Sales: {{ product.sales }}</p>
    </div>
    
    <div class="review-section">
      <h2>Submit Your Review</h2>
      
      <div class="submit-review">
        <form @submit.prevent="submitReview" class="review-form">
          
          <div class="form-group">
            <label for="rating">Rating:</label>
            <select v-model="newReview.rating" required class="select-input">
              <option value="">Select a rating</option>
              <option v-for="num in 5" :key="num" :value="num">{{ num }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="comment">Comment:</label>
            <textarea v-model="newReview.comment" required class="textarea-input"></textarea>
          </div>
          <button type="submit" class="submit-button">Submit Review</button>
        </form>
      </div>


    <h2>Reviews</h2>
      <div v-for="review in product.reviews" :key="review.id" class="review">
        <p>User: {{ review.username }}</p>
        <p>Rating: {{ review.rating }}</p>
        <p>Created Date: {{ new Date(review.review_date).toLocaleDateString() }}</p>
        <p>{{ review.comment }}</p>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    id: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      product: { reviews: [] },
      newReview: {
        rating: '',
        comment: ''
      }   
    };
  },

  mounted() {
    this.fetchProductDetails();
  },

  methods: {
    fetchProductDetails() {
      axios.get(`http://localhost:8000/api/shop/products/${this.id}/product_detail/`)
        .then(response => {
          this.product = response.data;
        })
        .catch(error => {
          console.error("Error fetching product details:", error);
        });
    },

    submitReview() {
      const reviewData = {
        rating: this.newReview.rating,
        comment: this.newReview.comment,
        review_date: new Date().toISOString() // ISO string for Django
      };
      axios.post(`http://localhost:8000/api/shop/products/${this.id}/submit_review/`, reviewData, { withCredentials: true })
        .then(() => {
          alert('Review submitted successfully!');
          this.fetchProductDetails(); // Refresh the reviews
        })
        .catch(error => {
          let errorMessage = "";
          // Check if the error response has the specific message
          if (error.response && error.response.data && error.response.data.error) {
              errorMessage += ` ${error.response.data.error}`;
          }
          console.error(errorMessage);
          alert(errorMessage); // Display the constructed error message
        });
    },

  }
}
</script>

<style scoped>
.product-detail-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.product-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 10px;
}

.review-section, .product-detail {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.review {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 10px;
}

.form-group select, .form-group textarea {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 16px;
  width: 100%;
}

.select-input, .textarea-input {
  margin: 10px 0;
}

.submit-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>
