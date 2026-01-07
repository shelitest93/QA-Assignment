pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Response structure is valid", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('page');
    pm.expect(jsonData).to.have.property('per_page');
    pm.expect(jsonData).to.have.property('data');
    pm.expect(Array.isArray(jsonData.data)).to.be.true;
});

pm.test("Verify page number matches query", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.page).to.eql(2);
});

pm.test("Each user has required fields", function () {
    const jsonData = pm.response.json();
    jsonData.data.forEach((user) => {
        pm.expect(user).to.have.property('id');
        pm.expect(user).to.have.property('email').and.include("@");
        pm.expect(user).to.have.property('avatar').and.include("https://");
    });
});