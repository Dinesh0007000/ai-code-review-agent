import { render, screen } from '@testing-library/react';
import App from './App';

test('renders AI Code Review Agent header', () => {
  render(<App />);
  const headerElement = screen.getByText(/AI Code Review Agent/i);
  expect(headerElement).toBeInTheDocument();
});
