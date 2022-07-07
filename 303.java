class NumArray {

    public NumArray(int[] nums) {
        p = new int[nums.length + 1];
        p[0] = 0;
        for(int i = 1; i < p.length; i++) {
            p[i] = p[i-1] + nums[i-1];
        }
    }
    
    public int sumRange(int left, int right) {
        return p[right+1] - p[left];
    }
    
    private int[] p;
}
