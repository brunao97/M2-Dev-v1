#pragma once
#include <string>

class CFileNameHelper
{
public:
	static void ChangeDosPath(std::string& str)
	{
		size_t nLength = str.length();

		for (size_t i = 0; i < nLength; ++i)
		{
			if (str.at(i) == '/')
			{
				str.at(i) = '\\';
			}
		}
	}

	static void StringPath(std::string& str)
	{
		size_t nLength = str.length();

		for (size_t i = 0; i < nLength; ++i)
		{
			if (str.at(i) == '\\')
			{
				str.at(i) = '/';
			}

			else
			{
				str.at(i) = (char)tolower(str.at(i));
			}
		}
	}

	static std::string GetName(std::string& str);          // if filename is "/idv/code/file.cpp", it returns "file"
	static std::string GetExtension(std::string& str);     // if filename is "/idv/code/file.cpp", it returns "cpp"
	static std::string GetPath(std::string& str);          // if filename is "/idv/code/file.cpp", it returns "/idv/code"
	static std::string NoExtension(std::string& str);      // if filename is "/idv/code/file.cpp", it returns "/idv/code/file"
	static std::string NoPath(std::string& str);           // if filename is "/idv/code/file.cpp", it returns "file.cpp"
};

///////////////////////////////////////////////////////////////////////
//	CFileNameHelper::GetExtension

inline std::string CFileNameHelper::GetName(std::string& str)
{
	std::string strName;

	size_t nLength = str.length();

	if (nLength > 0)
	{
		size_t iExtensionStartPos = nLength - 1;

		for (size_t i = nLength - 1; i > 0; i--)
		{
			if (str[i] == '.')
			{
				iExtensionStartPos = i;
			}

			if (str[i] == '/')
			{
				strName = std::string(str.c_str() + i + 1);
				strName.resize(iExtensionStartPos - i - 1);
				break;
			}
		}
	}

	return strName;
}

///////////////////////////////////////////////////////////////////////
//	CFilenameHelper::GetExtension

inline std::string CFileNameHelper::GetExtension(std::string& str)
{
	std::string strExtension;

	size_t nLength = str.length();

	if (nLength > 0)
	{
		for (size_t i = nLength - 1; i > 0 && str[i] != '/'; i--)
			if (str[i] == '.')
			{
				strExtension = std::string(str.c_str() + i + 1);
				break;
			}
	}

	return strExtension;
}

///////////////////////////////////////////////////////////////////////
//	CFilenameHelper::GetPath

inline std::string CFileNameHelper::GetPath(std::string& str)
{
	char szPath[1024];
	szPath[0] = '\0';

	size_t nLength = str.length();

	if (nLength > 0)
	{
		for (size_t i = nLength - 1; i > 0; i--)
		{
			if (str[i] == '/' || str[i] == '\\')
			{
				for (size_t j = 0; j < i + 1; j++)
				{
					szPath[j] = str[j];
				}

				szPath[i + 1] = '\0';
				break;
			}

			if (0 == i)
			{
				break;
			}
		}
	}

	return szPath;
}

///////////////////////////////////////////////////////////////////////
//	CFilenameHelper::NoExtension

inline std::string CFileNameHelper::NoExtension(std::string& str)
{
	std::size_t npos = str.find_last_of('.');

	if (std::string::npos != npos)
	{
		return std::string(str, 0, npos);
	}

	return str;
}

///////////////////////////////////////////////////////////////////////
//	CFilenameHelper::NoPath

inline std::string CFileNameHelper::NoPath(std::string& str)
{
	char szPath[1024];
	szPath[0] = '\0';

	size_t nLength = str.length();

	if (nLength > 0)
	{
		strcpy(szPath, str.c_str());

		for (size_t i = nLength - 1; i > 0; i--)
		{
			if (str[i] == '/' || str[i] == '\\')
			{
				int k = 0;

				for (size_t j = i + 1; j < nLength; j++, k++)
				{
					szPath[k] = str[j];
				}

				szPath[k] = '\0';
				break;
			}

			if (0 == i)
			{
				break;
			}
		}
	}

	return szPath;
}