import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders air traffic control system', () => {
  render(<App />);
  const titleElement = screen.getByText(/Air Traffic Control System/i);
  expect(titleElement).toBeInTheDocument();
});
