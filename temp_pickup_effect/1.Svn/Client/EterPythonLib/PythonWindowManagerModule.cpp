//Find
void initwndMgr()

///Add Above
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
PyObject* wndMgrSetSlotDiffuseColor(PyObject* poSelf, PyObject* poArgs)
{
	UI::CWindow* pWindow;
	if (!PyTuple_GetWindow(poArgs, 0, &pWindow))
		return Py_BuildException();
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BuildException();
	int iColorType;
	if (!PyTuple_GetInteger(poArgs, 2, &iColorType))
		return Py_BuildException();

	if (!pWindow->IsType(UI::CSlotWindow::Type()))
		return Py_BuildException();

	((UI::CSlotWindow*)pWindow)->SetSlotDiffuseColor(iIndex, iColorType);
	return Py_BuildNone();
}
#endif

//Find
		{ "SetSlotCount",				wndMgrSetSlotCount,					METH_VARARGS },

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
		{ "SetSlotDiffuseColor",		wndMgrSetSlotDiffuseColor,			METH_VARARGS },
#endif

//Find
	PyModule_AddIntConstant(poModule, "RENDERING_MODE_MODULATE",		CGraphicExpandedImageInstance::RENDERING_MODE_MODULATE);

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_ORANGE", UI::COLOR_TYPE_ORANGE);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_WHITE", UI::COLOR_TYPE_WHITE);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_RED", UI::COLOR_TYPE_RED);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_GREEN", UI::COLOR_TYPE_GREEN);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_YELLOW", UI::COLOR_TYPE_YELLOW);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_SKY", UI::COLOR_TYPE_SKY);
	PyModule_AddIntConstant(poModule, "COLOR_TYPE_PINK", UI::COLOR_TYPE_PINK);

	PyModule_AddIntConstant(poModule, "HILIGHTSLOT_ACCE", UI::HILIGHTSLOT_ACCE);
	PyModule_AddIntConstant(poModule, "HILIGHTSLOT_CHANGE_LOOK", UI::HILIGHTSLOT_CHANGE_LOOK);
	PyModule_AddIntConstant(poModule, "HILIGHTSLOT_AURA", UI::HILIGHTSLOT_AURA);
	PyModule_AddIntConstant(poModule, "HILIGHTSLOT_CUBE", UI::HILIGHTSLOT_CUBE);
	PyModule_AddIntConstant(poModule, "HILIGHTSLOT_MAX", UI::HILIGHTSLOT_MAX);
#endif