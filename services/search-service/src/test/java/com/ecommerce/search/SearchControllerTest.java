package com.ecommerce.search.controller;

import com.ecommerce.search.dto.SearchQueryRequest;
import com.ecommerce.search.dto.SearchQueryResponse;
import com.ecommerce.search.service.SearchService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class SearchControllerTest {

    @Mock
    private SearchService service;

    @InjectMocks
    private SearchController controller;

    @Test
    void getQueries_shouldReturnList() {
        SearchQueryResponse response = new SearchQueryResponse();
        response.setId(1L);
        response.setQuery("laptop");
        response.setUserId(1L);

        when(service.getQueriesByUserId(1L)).thenReturn(List.of(response));

        List<SearchQueryResponse> result = controller.getQueries(1L);

        assertEquals(1, result.size());
        assertEquals("laptop", result.get(0).getQuery());
    }

    @Test
    void saveQuery_shouldReturnResponse() {
        SearchQueryRequest request = new SearchQueryRequest();
        request.setQuery("phone");
        request.setUserId(2L);

        SearchQueryResponse response = new SearchQueryResponse();
        response.setId(1L);
        response.setQuery("phone");
        response.setUserId(2L);

        when(service.saveQuery(request)).thenReturn(response);

        SearchQueryResponse result = controller.saveQuery(request);

        assertNotNull(result);
        assertEquals("phone", result.getQuery());
    }

    @Test
    void getAllQueries_shouldReturnAll() {
        SearchQueryResponse response = new SearchQueryResponse();
        response.setId(1L);
        response.setQuery("laptop");

        when(service.getAllQueries()).thenReturn(List.of(response));

        List<SearchQueryResponse> result = controller.getAllQueries();

        assertEquals(1, result.size());
    }
}
