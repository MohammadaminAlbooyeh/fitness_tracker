package com.ecommerce.common;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class BaseEntityTest {

    @Test
    void baseEntityHasIdField() {
        BaseEntity entity = new BaseEntity() {};
        assertNull(entity.getId());
    }

    @Test
    void baseEntityHasTimestamps() {
        BaseEntity entity = new BaseEntity() {};
        assertNull(entity.getCreatedAt());
        assertNull(entity.getUpdatedAt());
    }

    @Test
    void baseEntityCanSetFields() {
        BaseEntity entity = new BaseEntity() {};
        LocalDateTime now = LocalDateTime.now();
        entity.setId(1L);
        entity.setCreatedAt(now);
        entity.setUpdatedAt(now);

        assertEquals(1L, entity.getId());
        assertEquals(now, entity.getCreatedAt());
        assertEquals(now, entity.getUpdatedAt());
    }
}
