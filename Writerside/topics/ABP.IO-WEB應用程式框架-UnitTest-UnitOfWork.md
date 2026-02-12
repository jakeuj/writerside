# ABP.IO UnitTest UnitOfWork

> **原文發布日期:** 2022-10-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/28/abp--UnitTest-UnitOfWork
> **標籤:** 無

---

筆記下單元測試的 UOW 使用姿勢

## 結論

```
[Fact]
public async Task Should_Get_A_Data_From_DataSeed()
{
    var identityUserRepository = GetRequiredService<IIdentityUserRepository>();

    //Act
    var result = await WithUnitOfWorkAsync(async () =>
        await identityUserRepository.FirstOrDefaultAsync());

    //Assert
    result.ShouldNotBeNull();
}
```

### 範例

SampleDomainTests.cs

```
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp.Identity;
using Xunit;

namespace TestProject.Samples;

/* This is just an example test class.
 * Normally, you don't test code of the modules you are using
 * (like IdentityUserManager here).
 * Only test your own domain services.
 */
public class SampleDomainTests : TestProjectDomainTestBase
{
    private readonly IIdentityUserRepository _identityUserRepository;
    private readonly IdentityUserManager _identityUserManager;

    public SampleDomainTests()
    {
        _identityUserRepository = GetRequiredService<IIdentityUserRepository>();
        _identityUserManager = GetRequiredService<IdentityUserManager>();
    }

    [Fact]
    public async Task Should_Set_Email_Of_A_User()
    {
        IdentityUser adminUser;

        /* Need to manually start Unit Of Work because
         * FirstOrDefaultAsync should be executed while db connection / context is available.
         */
        await WithUnitOfWorkAsync(async () =>
        {
            adminUser = await _identityUserRepository
                .FindByNormalizedUserNameAsync("ADMIN");

            await _identityUserManager.SetEmailAsync(adminUser, "newemail@abp.io");
            await _identityUserRepository.UpdateAsync(adminUser);
        });

        adminUser = await _identityUserRepository.FindByNormalizedUserNameAsync("ADMIN");
        adminUser.Email.ShouldBe("newemail@abp.io");
    }
}
```

官方文件

```
public class IssueRepository_Tests : MyProjectDomainTestBase
{
    private readonly IRepository<Issue, Guid> _issueRepository;
    private readonly IUnitOfWorkManager _unitOfWorkManager;

    public IssueRepository_Tests()
    {
        _issueRepository = GetRequiredService<IRepository<Issue, Guid>>();
        _unitOfWorkManager = GetRequiredService<IUnitOfWorkManager>();
    }

    public async Task Should_Query_By_Title()
    {
        using (var uow = _unitOfWorkManager.Begin())
        {
            IQueryable<Issue> queryable = await _issueRepository.GetQueryableAsync();
            var issue = queryable.FirstOrDefaultAsync(i => i.Title == "My issue title");
            issue.ShouldNotBeNull();
            await uow.CompleteAsync();
        }
    }
}
```

參照

[Testing | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Testing#dealing-with-unit-of-work-in-integration-tests)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- UnitTest

- 回首頁

---

*本文章從點部落遷移至 Writerside*
