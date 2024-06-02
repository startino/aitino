export const sum = (nums) => nums.reduce((a, b) => a + b, 0);
export const mean = (nums) => (nums.length === 0 ? 0 : sum(nums) / nums.length);
