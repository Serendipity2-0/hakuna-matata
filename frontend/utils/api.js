// utils/api.js
import axios from './axios'; // Your custom axios instance

export const getDepartments = async () => {
  const response = await axios.get('/list-of-departments');
  return response.data.departments;
};
