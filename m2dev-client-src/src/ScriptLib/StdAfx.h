#pragma once

#include "EterLib/StdAfx.h"
#include "EterGrnLib/StdAfx.h"

//#include <crtdbg.h>
#ifdef _DEBUG
#undef _DEBUG
#include <python/python.h>
#define _DEBUG
#else
#include <python/python.h>
#endif
#include <python/node.h>
#include <python/grammar.h>
#include <python/token.h>
#include <python/parsetok.h>
#include <python/errcode.h>
#include <python/compile.h>
#include <python/eval.h>
#include <python/marshal.h>

#ifdef BYTE
#undef BYTE
#endif

#include "PythonUtils.h"
#include "PythonLauncher.h"
#include "Resource.h"

void initdbg();
