# Flutter 使用 aad_oauth 整合 Azure AD 登入

<web-summary>使用 Flutter aad_oauth 套件整合 Azure AD 登入，設定 tenant、clientId、redirectUri 與 scope，取得 ID token 並解析使用者資料。</web-summary>

This Flutter application demonstrates how to implement Azure Active Directory (Azure AD) login using the `aad_oauth` package.
It allows users to log in with their Azure AD credentials and displays their profile information.

## Dependencies

```yaml
dependencies:
  aad_oauth: ^1.0.0
```

## Sample Code

```dart
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:aad_oauth/aad_oauth.dart';
import 'package:aad_oauth/model/config.dart';

void main() {
  runApp(const MyApp());
}

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Azure AD Login',
      home: const LoginPage(),
      navigatorKey: navigatorKey,
    );
  }
}

class AuthService {
  static const String tenantId = 'xxxx-xxxx-xxxx-xxxx-xxxx';
  static const String clientId = 'xxxx-xxxx-xxxx-xxxx-xxxx';
  static const String redirectUri = 'https://login.live.com/oauth20_desktop.srf';
  static const String scope = 'openid profile email';

  static AadOAuth get oauth => AadOAuth(
        Config(
          tenant: tenantId,
          clientId: clientId,
          redirectUri: redirectUri,
          navigatorKey: navigatorKey,
          scope: scope,
        ),
      );
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final AadOAuth _oauth = AuthService.oauth;
  bool _isLoading = false;

  Future<void> login() async {
    setState(() => _isLoading = true);
    try {
      await _oauth.login();
      await _oauth.getAccessToken(); // 可省略但保留
      final idToken = await _oauth.getIdToken();

      if (!mounted || idToken == null) return;

      final userInfo = _parseIdToken(idToken);
      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ProfilePage(userInfo: userInfo),
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('登入失敗: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Map<String, dynamic> _parseIdToken(String token) {
    final payload = token.split('.')[1];
    final normalized = base64Url.normalize(payload);
    final decoded = utf8.decode(base64Url.decode(normalized));
    return json.decode(decoded);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Azure AD 登入')),
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator()
            : ElevatedButton(
                onPressed: login,
                child: const Text('使用 Azure AD 登入'),
              ),
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  final Map<String, dynamic> userInfo;

  const ProfilePage({super.key, required this.userInfo});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('使用者資訊'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await AuthService.oauth.logout();
              if (context.mounted) Navigator.pop(context);
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                radius: 50,
                backgroundColor: Colors.blue.shade100,
                child: Text(
                  _getInitials(),
                  style: TextStyle(fontSize: 40, color: Colors.blue.shade800),
                ),
              ),
            ),
            const SizedBox(height: 20),
            _buildInfoCard('姓名', userInfo['name'] ?? '未提供'),
            _buildInfoCard(
              '信箱',
              userInfo['email'] ?? userInfo['preferred_username'] ?? '未提供',
            ),
            _buildInfoCard(
              '使用者 ID',
              userInfo['oid'] ?? userInfo['sub'] ?? '未提供',
            ),
            if (userInfo['roles'] != null)
              _buildInfoCard(
                '角色',
                (userInfo['roles'] as List<dynamic>).join(', '),
              ),
          ],
        ),
      ),
    );
  }

  String _getInitials() {
    final name = userInfo['name'] ?? userInfo['preferred_username'] ?? '';
    final parts = (name as String).split(' ');
    return parts.length >= 2
        ? '${parts.first[0]}${parts.last[0]}'.toUpperCase()
        : name.isNotEmpty
            ? name[0].toUpperCase()
            : '?';
  }

  Widget _buildInfoCard(String label, String value) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontSize: 14, color: Colors.grey)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
```

## AAD redirect URL

登入時會根據 Azure AD 設定的 redirect url 判斷是 web 或是 mobile，登入流程分別會是需要 secret 或是 public client。
因為手機不應該使用 client secret，所以這邊使用的是 public client。
Azure AD 上的應用程式登入設定下方有內建三個桌面與手機應用的 redirect url，可以直接勾選啟用。
這三個 AAD redirect URL 各自代表了不同的用法與支援的登入流程，以下是針對 Flutter 手機 App 使用時的差異分析：

⸻

🔵 `https://login.microsoftonline.com/common/oauth2/nativeclient`

- • 用途：這是 Microsoft 官方推薦給「原生 App（Native App）」使用的 通用 redirect URI。
- • 適用於：
- • MSAL (Microsoft Authentication Library)
- • 原生行動應用程式（Android / iOS）
- • 特性：
- • 不需要自訂 URI scheme。
- • 適合於「公共用戶端（public client）」情境，例如行動裝置不適合儲存 secret。
- • 搭配 MSAL，可以啟動系統內建瀏覽器或自動導向到 Microsoft 登入頁。
- • 注意：
- • 若你是用 Flutter + MSAL plugin（如 msal_flutter），通常不會使用這個，因為插件會使用自訂 scheme。

⸻

🟡 `https://login.live.com/oauth20_desktop.srf`（LiveSDK）

- • 用途：這是過去 Live SDK（已淘汰） 使用的 redirect URI。
- • 適用於：
- • 舊的 Live SDK 登入流程（現在已被 MSAL/Graph API 所取代）
- • 特性：
- • 現代 App 不建議再使用這個 URI。
- • 注意：
- • 幾乎已經過時，現在開發新的 App 應完全改用 MSAL 或 Microsoft Entra ID（Azure AD）。

⸻

🟢 `msal<client-id>://auth`（自訂 URI Scheme）

- • 用途：這是 原生應用最常見的 redirect URI 寫法，是 Deep Link / App Linking 的一種。
- • 適用於：
- • 使用 MSAL 登入流程，尤其是原生 App 或 Flutter App。
- • 特性：
- • 需要在 App 註冊對應的 URI scheme（Android 的 intent filter，iOS 的 URL types）。
- • 這個 redirect URI 必須在 Azure AD App 註冊中設定，否則會登入失敗。
- • 例如你註冊的 app ID 是 xxxx-xxxx-xxxx-xxxx-xxxx，那麼你可以設成：

```
msalxxxx-xxxx-xxxx-xxxx-xxxx://auth
```

- • Flutter 注意事項：
- • 搭配 msal_flutter 或 flutter_appauth 等套件使用這個最方便。
- • 記得要在 AndroidManifest.xml 和 Info.plist 配置 URI scheme。

⸻

✅ Flutter 建議使用哪個？

✅ 最佳實務：使用 `msal<client-id>://auth`

- ✔️ 易於整合 App 自身的登入處理
- ✔️ 可讓登入後跳回你的 App
- ✔️ 支援 Flutter 插件（如 msal_flutter, flutter_appauth）
- ✔️ 可用於 Deep Linking、進一步整合 App Navigation

⸻

🔚 總結比較表：

| Redirect URI | 適用場景 | Flutter 推薦？ | 備註 |
|-------------|---------|-------------|------|
| `https://login.microsoftonline.com/...` | 通用原生 App | ❌ | 比較老派寫法，難與 Flutter Deep Link 配合 |
| `https://login.live.com/oauth20_desktop.srf` | Live SDK（淘汰） | ❌ | 不再建議使用 |
| `msal<client-id>://auth` | Flutter 手機 App | ✅ | 推薦使用，支援 App Redirect，自訂 scheme |
