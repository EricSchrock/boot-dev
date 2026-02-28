package main

import "testing"

func TestCleanInput(t *testing.T) {
	cases := []struct {
		input    string
		expected []string
	}{
		{
			input:    "test",
			expected: []string{"test"},
		},
		{
			input:    "test ",
			expected: []string{"test"},
		},
		{
			input:    "test  ",
			expected: []string{"test"},
		},
		{
			input:    "test \t",
			expected: []string{"test"},
		},
		{
			input:    " test",
			expected: []string{"test"},
		},
		{
			input:    "   test",
			expected: []string{"test"},
		},
		{
			input:    "\t \rtest",
			expected: []string{"test"},
		},
		{
			input:    "test test",
			expected: []string{"test", "test"},
		},
		{
			input:    "test1 test2",
			expected: []string{"test1", "test2"},
		},
		{
			input:    "test1\r\ntest2",
			expected: []string{"test1", "test2"},
		},
		{
			input:    "test1  test2",
			expected: []string{"test1", "test2"},
		},
		{
			input:    "test1 test2 test3",
			expected: []string{"test1", "test2", "test3"},
		},
		{
			input:    "Test1 tEst2 TEST3",
			expected: []string{"test1", "test2", "test3"},
		},
	}

	for _, c := range cases {
		actual := cleanInput(c.input)

		if len(actual) != len(c.expected) {
			t.Errorf("len(actual)=%v != len(expected)=%v", len(actual), len(c.expected))
		}

		for i := range actual {
			if actual[i] != c.expected[i] {
				t.Errorf("actual[%v]=%s != expected[%v]=%s", i, actual[i], i, c.expected[i])
			}
		}
	}
}
