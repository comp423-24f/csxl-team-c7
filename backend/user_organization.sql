CREATE TABLE user_organization (
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    role VARCHAR(255),
    PRIMARY KEY (user_id, organization_id),
    FOREIGN KEY (user_id) REFERENCES "user" (id),
    FOREIGN KEY (organization_id) REFERENCES "organization" (id)
);
