import '@testing-library/jest-dom';
import { Dashboard } from 'features/Dashboard/Dashboard';
import { setupServer } from 'msw/node';
import React, { createElement } from 'react';
import { cleanup, renderWithProviders, screen } from 'test-utils';
import { mockUserEndpoints } from 'test-utils/mock';
import { mockSiteEndpoints } from 'test-utils/mock/mockSiteEndpoints';
import { afterAll, afterEach, beforeAll, describe, expect, test, vi } from 'vitest';

const USERNAME = 'testuser1';

const server = setupServer(...mockSiteEndpoints, ...mockUserEndpoints);

beforeAll(() => {
  vi.mock('recharts', async (importOriginal) => {
    const originalModule = (await importOriginal()) as Record<string, unknown>;
    return {
      ...originalModule,
      ResponsiveContainer: () => createElement('div'),
    };
  });
  server.listen();
}); // setup mock http server
afterEach(() => {
  server.resetHandlers();
  cleanup();
  vi.resetAllMocks();
});
afterAll(() => server.close()); // Disable API mocking after the tests are done.

describe('Home', () => {
  test('renders', () => {
    renderWithProviders(<Dashboard />, {
      preloadedState: {
        auth: {
          user: { username: USERNAME, isLoading: false },
          token: 'fake_token',
          loading: false,
          error: undefined,
        },
      },
    });
    expect(screen.getByText(/Welcome/i)).toBeInTheDocument();
  });
});
