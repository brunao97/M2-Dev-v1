//Find
	void CAniImageBox::SetDelay(int iDelay)
	{
		...
	}

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	void CAniImageBox::SetDiffuseColor(float r, float g, float b, float a)
	{
		for (CGraphicExpandedImageInstance* image : m_ImageVector)
			image->SetDiffuseColor(r, g, b, a);
	}
#endif