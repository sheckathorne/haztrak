import '@testing-library/jest-dom';
import { MtnTable } from 'components/Mtn';
import React from 'react';
import { cleanup, renderWithProviders, screen } from 'test-utils';
import { MtnDetails } from 'components/Mtn';

const manifestDetail: MtnDetails = {
  manifestTrackingNumber: '123456789ELC',
  status: 'InTransit',
};

const mtnData = [manifestDetail, manifestDetail];

afterEach(() => {
  cleanup();
});

describe('MtnTable', () => {
  test('renders', async () => {
    renderWithProviders(<MtnTable manifests={mtnData} />);
    expect(await screen.findAllByText(manifestDetail.manifestTrackingNumber)).toHaveLength(2);
  });
});