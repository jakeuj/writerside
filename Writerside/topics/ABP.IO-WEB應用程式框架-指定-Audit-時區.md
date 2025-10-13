# ABP.IO WEB應用程式框架 指定 Audit 時區

> **原文發布日期:** 2023-01-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/09/ABP-Audit-TimeZone-Pacific-Standard-Time
> **標籤:** 無

---

指定審計使用太平洋標準時間 (CreationTime…ETC)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/570f744e-c327-4e46-b680-7b38c0b55e86/1673922949.png.png)

結論

[CustomAuditPropertySetter](https://github.com/abpframework/abp/blob/dev/framework/src/Volo.Abp.Auditing/Volo/Abp/Auditing/AuditPropertySetter.cs)

```
using System;
using Volo.Abp;
using Volo.Abp.Auditing;
using Volo.Abp.MultiTenancy;
using Volo.Abp.Timing;
using Volo.Abp.Users;

namespace Volo.Abp.Auditing;

public class CustomAuditPropertySetter : AuditPropertySetter
{
    private const string TimeZone = "Pacific Standard Time";
    private readonly TimeZoneInfo _timeZoneInfo;

    public CustomAuditPropertySetter(
        ICurrentUser currentUser,
        ICurrentTenant currentTenant,
        IClock clock,
        ITimezoneProvider timezoneProvider
    ) : base(currentUser, currentTenant, clock)
    {
        _timeZoneInfo = timezoneProvider.GetTimeZoneInfo(TimeZone);
    }

    private DateTime TimeZoneConverter()
    {
        return TimeZoneInfo.ConvertTime(
            Clock.Now.ToUniversalTime(), _timeZoneInfo);
    }
    private DateTime? NullableTimeZoneConverter()
    {
        return TimeZoneConverter();
    }

    protected override void SetCreationTime(object targetObject)
    {
        if (!(targetObject is IHasCreationTime objectWithCreationTime))
        {
            return;
        }

        if (objectWithCreationTime.CreationTime == default)
        {
            ObjectHelper.TrySetProperty(objectWithCreationTime, x =>
                x.CreationTime, TimeZoneConverter);
        }
    }

    protected override void SetLastModificationTime(object targetObject)
    {
        if (targetObject is IHasModificationTime objectWithModificationTime)
        {
            ObjectHelper.TrySetProperty(objectWithModificationTime, x =>
                x.LastModificationTime, NullableTimeZoneConverter);
        }
    }

    protected override void SetDeletionTime(object targetObject)
    {
        if (targetObject is IHasDeletionTime objectWithDeletionTime)
        {
            if (objectWithDeletionTime.DeletionTime == null)
            {
                ObjectHelper.TrySetProperty(objectWithDeletionTime, x =>
                    x.DeletionTime, NullableTimeZoneConverter);
            }
        }
    }
}
```

AbpModule

```
context.Services.Replace(ServiceDescriptor.Transient
    <IAuditPropertySetter, CustomAuditPropertySetter>());
Configure<AbpClockOptions>(options => { options.Kind = DateTimeKind.Utc; });
```

參照

[c# - How to set ABP.IO IHasCreationTime for TimeZone 'Pacific Standard Time' (EF and SQL Server)](https://stackoverflow.com/questions/75039614/how-to-set-abp-io-ihascreationtime-for-timezone-pacific-standard-time-ef-and)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* Audit
* TimeZone

* 回首頁

---

*本文章從點部落遷移至 Writerside*
