#include "StdAfx.h"

#include <stdio.h>
#include <time.h>
#include <winsock.h>
#include <imagehlp.h>

FILE* fException;

#if _MSC_VER >= 1400
BOOL CALLBACK EnumerateLoadedModulesProc(PCSTR ModuleName, ULONG ModuleBase, ULONG ModuleSize, PVOID UserContext)
#else
BOOL CALLBACK EnumerateLoadedModulesProc(PSTR ModuleName, ULONG ModuleBase, ULONG ModuleSize, PVOID UserContext)
#endif
{
	DWORD offset = *((DWORD*)UserContext);

	if (offset >= ModuleBase && offset <= ModuleBase + ModuleSize)
	{
		fprintf(fException, "%s", ModuleName);
		//__idx += sprintf(__msg+__idx, "%s", ModuleName);
		return FALSE;
	}

	else
	{
		return TRUE;
	}
}

LONG __stdcall EterExceptionFilter(_EXCEPTION_POINTERS* pExceptionInfo)
{
	HANDLE		hProcess = GetCurrentProcess();
	HANDLE		hThread = GetCurrentThread();

	fException = fopen("log/ErrorLog.txt", "wt");

	if (fException)
	{
		char module_name[256];
		time_t module_time;

		HMODULE hModule = GetModuleHandle(NULL);

		GetModuleFileName(hModule, module_name, sizeof(module_name));
		module_time = (time_t)GetTimestampForLoadedLibrary(hModule);

		fprintf(fException, "Module Name: %s\n", module_name);
		fprintf(fException, "Time Stamp: 0x%08x - %s\n", (unsigned int)module_time, ctime(&module_time));
		fprintf(fException, "\n");
		fprintf(fException, "Exception Type: 0x%08x\n", pExceptionInfo->ExceptionRecord->ExceptionCode);
		fprintf(fException, "\n");

		CONTEXT& context = *pExceptionInfo->ContextRecord;
		fprintf(fException, "rax: 0x%016llx\trbx: 0x%016llx\n", context.Rax, context.Rbx);
		fprintf(fException, "rcx: 0x%016llx\trdx: 0x%016llx\n", context.Rcx, context.Rdx);
		fprintf(fException, "rsi: 0x%016llx\trdi: 0x%016llx\n", context.Rsi, context.Rdi);
		fprintf(fException, "rbp: 0x%016llx\trsp: 0x%016llx\n", context.Rbp, context.Rsp);
		fprintf(fException, "\n");

		STACKFRAME64 stackFrame = { 0 };
		stackFrame.AddrPC.Offset = context.Rip;
		stackFrame.AddrPC.Mode = AddrModeFlat;
		stackFrame.AddrStack.Offset = context.Rsp;
		stackFrame.AddrStack.Mode = AddrModeFlat;
		stackFrame.AddrFrame.Offset = context.Rbp;
		stackFrame.AddrFrame.Mode = AddrModeFlat;

		for (int i = 0; i < 512 && stackFrame.AddrPC.Offset; ++i)
		{
			if (StackWalk64(IMAGE_FILE_MACHINE_AMD64, hProcess, hThread, &stackFrame, &context, NULL, SymFunctionTableAccess64, SymGetModuleBase64, NULL) != FALSE)
			{
				fprintf(fException, "0x%016llx\t", stackFrame.AddrPC.Offset);
				//__idx+=sprintf(__msg+__idx, "0x%016llx\t", stackFrame.AddrPC.Offset);
				EnumerateLoadedModules64(hProcess, (PENUMLOADED_MODULES_CALLBACK64)EnumerateLoadedModulesProc, &stackFrame.AddrPC.Offset);
				fprintf(fException, "\n");

				//__idx+=sprintf(__msg+__idx,  "\n");
			}

			else
			{
				break;
			}
		}

		fprintf(fException, "\n");

		fflush(fException);

		fclose(fException);
		fException = NULL;

		WinExec("errorlog.exe", SW_SHOW);
	}

	return EXCEPTION_EXECUTE_HANDLER;
}

void SetEterExceptionHandler()
{
	SetUnhandledExceptionFilter(EterExceptionFilter);
}