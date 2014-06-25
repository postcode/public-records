describe("A Query model", function() {
  it('should be able to create its application test objects',
   function() {
      var query = new Query();
      expect(query).toBeDefined();
      expect(MOCK_GET_DATA).toBeDefined();
      expect(MOCK_POST_DATA).toBeDefined();
  });
});
