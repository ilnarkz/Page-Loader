import pytest

from page_loader.naming import get_name, get_dir_name, get_html_file_name


@pytest.mark.parametrize('received, expected', [('google.com', 'google-com'),
                                                ('ru.hexlet.io', 'ru-hexlet-io'),
                                                ('ru.code-basics.com/languages/python', 'ru-code-basics-com-languages-python')])
def test_get_name(received, expected):
    assert get_name(received) == expected


@pytest.mark.parametrize('received, expected', [('google.com', 'google-com.html'),
                                                ('ru.hexlet.io', 'ru-hexlet-io.html'),
                                                ('ru.code-basics.com/languages/python', 'ru-code-basics-com-languages-python.html'),
                                                ('https://google.com/index.html', 'google-com-index.html')])
def test_get_html_file_name(received, expected):
    assert get_html_file_name(received) == expected


@pytest.mark.parametrize('received, expected', [('google-com', 'google-com_files'),
                                                ('ru-hexlet-io', 'ru-hexlet-io_files'),
                                                ('ru-code-basics-com-languages-python', 'ru-code-basics-com-languages-python_files')])
def test_get_dir_name(received, expected):
    assert get_dir_name(received) == expected