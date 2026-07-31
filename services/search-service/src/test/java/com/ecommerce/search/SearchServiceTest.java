package com.ecommerce.search.service;

import com.ecommerce.search.dto.SearchQueryRequest;
import com.ecommerce.search.dto.SearchQueryResponse;
import com.ecommerce.search.entity.SearchQuery;
import com.ecommerce.search.repository.SearchQueryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SearchServiceTest {

    @Mock
    private SearchQueryRepository repository;

    @InjectMocks
    private SearchService service;

    private SearchQueryRequest request;

    @BeforeEach
    void setUp() {
        request = new SearchQueryRequest();
        request.setQuery("laptop");
        request.setUserId(1L);
    }

    @Test
    void saveQuery_shouldSaveAndReturnResponse() {
        SearchQuery saved = new SearchQuery();
        saved.setId(1L);
        saved.setQuery("laptop");
        saved.setUserId(1L);

        when(repository.save(any(SearchQuery.class))).thenReturn(saved);

        SearchQueryResponse response = service.saveQuery(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("laptop", response.getQuery());
        assertEquals(1L, response.getUserId());
        verify(repository).save(any(SearchQuery.class));
    }

    @Test
    void getQueriesByUserId_shouldReturnList() {
        SearchQuery query1 = new SearchQuery();
        query1.setId(1L);
        query1.setQuery("laptop");
        query1.setUserId(1L);

        SearchQuery query2 = new SearchQuery();
        query2.setId(2L);
        query2.setQuery("phone");
        query2.setUserId(1L);

        when(repository.findByUserId(1L)).thenReturn(List.of(query1, query2));

        List<SearchQueryResponse> responses = service.getQueriesByUserId(1L);

        assertEquals(2, responses.size());
        assertEquals("laptop", responses.get(0).getQuery());
        assertEquals("phone", responses.get(1).getQuery());
    }

    @Test
    void getAllQueries_shouldReturnAll() {
        SearchQuery query1 = new SearchQuery();
        query1.setId(1L);
        query1.setQuery("laptop");
        query1.setUserId(1L);

        SearchQuery query2 = new SearchQuery();
        query2.setId(2L);
        query2.setQuery("phone");
        query2.setUserId(2L);

        when(repository.findAll()).thenReturn(List.of(query1, query2));

        List<SearchQueryResponse> responses = service.getAllQueries();

        assertEquals(2, responses.size());
    }
}
