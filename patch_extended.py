#!/usr/bin/env python3
import os

print("[*] Applying KAMUI Extended enhancements...")

# 1. Update GestaltVC.m
gestalt_path = 'src/GestaltVC.m'
if os.path.exists(gestalt_path):
    with open(gestalt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    target_presets = '        @{@"title": NSLocalizedString(@"Disable Parallax", nil), @"keys": @[@"UIParallaxCapability"], @"value": @NO},\n    ];'
    new_presets = '''        @{@"title": NSLocalizedString(@"Disable Parallax", nil), @"keys": @[@"UIParallaxCapability"], @"value": @NO},
        @{@"title": NSLocalizedString(@"Mute Shutter Sound", nil), @"keys": @[@"h63QSdBCiT/z0WU6rdQv6Q"], @"value": @"US"},
        @{@"title": NSLocalizedString(@"Camera Control Button", nil), @"keys": @[@"CwvKxM2cEogD3p+HYgaW0Q", @"oOV1jhJbdV3AddkcCg0AEA"], @"value": @YES, @"minOS": @18},
        @{@"title": NSLocalizedString(@"Lockscreen Dimming (LGLPM)", nil), @"keys": @[@"SAGvsp6O6kAQ4fEfDJpC4Q"], @"value": @YES},
        @{@"title": NSLocalizedString(@"iPad Apps on iPhone", nil), @"keys": @[@"9MZ5AdH43csAUajl/dU+IQ"], @"value": @[@1, @2]},
    ];'''
    if target_presets in content:
        content = content.replace(target_presets, new_presets, 1)
        with open(gestalt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[+] GestaltVC.m presets patched")
    else:
        print("[!] target_presets already patched or not found")

# 2. Update SettingsVC.m
settings_path = 'src/SettingsVC.m'
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        s_content = f.read()

    clean_method = '''- (void)cleanCaches {
    BQConfirm(self, NSLocalizedString(@"Clean Caches?", nil),
              NSLocalizedString(@"Delete temporary caches across app containers to free storage.", nil), ^{
        BQBusyView *busy = [BQBusyView showInView:self.view text:NSLocalizedString(@"Cleaning caches...", nil)];
        dispatch_async(BQWorkQueue(), ^{
            __block NSUInteger cleanedCount = 0;
            NSArray<NSString *> *roots = @[
                @"/var/mobile/Containers/Data/Application",
                @"/var/mobile/Containers/Shared/AppGroup"
            ];
            for (NSString *root in roots) {
                NSArray<NSString *> *containers = BQListContainers(root);
                for (NSString *c in containers) {
                    NSString *cacheRel = @"Library/Caches";
                    NSString *err = nil;
                    NSArray<NSString *> *items = BQListPath(c, cacheRel, &err);
                    for (NSString *item in items) {
                        if ([item containsString:@"MobileGestalt"] || [item containsString:@"OriginalGestalt"]) continue;
                        NSString *subPath = [cacheRel stringByAppendingPathComponent:item];
                        if (BQDeletePath(c, subPath, &err)) {
                            cleanedCount++;
                        }
                    }
                }
            }
            dispatch_async(dispatch_get_main_queue(), ^{
                [busy hide];
                NSString *msg = [NSString stringWithFormat:NSLocalizedString(@"Cleaned %lu cache items across app containers.", nil), (unsigned long)cleanedCount];
                BQAlert(self, NSLocalizedString(@"Cache Cleaned", nil), msg);
            });
        });
    });
}

#pragma mark - Table'''

    if '#pragma mark - Table' in s_content and 'cleanCaches' not in s_content:
        s_content = s_content.replace('#pragma mark - Table', clean_method, 1)
        s_content = s_content.replace('case 2: return 2;', 'case 2: return 3;', 1)

        old_cell = '''        UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"tool"];
        if (!cell) cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"tool"];
        cell.textLabel.text = indexPath.row == 0 ? NSLocalizedString(@"Respring", nil) : NSLocalizedString(@"Open Log", nil);
        cell.textLabel.textColor = self.view.tintColor;
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
        return cell;'''

        new_cell = '''        UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"tool"];
        if (!cell) cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"tool"];
        if (indexPath.row == 0) {
            cell.textLabel.text = NSLocalizedString(@"Respring", nil);
            cell.textLabel.textColor = self.view.tintColor;
        } else if (indexPath.row == 1) {
            cell.textLabel.text = NSLocalizedString(@"Clean App Caches", nil);
            cell.textLabel.textColor = [UIColor systemOrangeColor];
        } else {
            cell.textLabel.text = NSLocalizedString(@"Open Log", nil);
            cell.textLabel.textColor = self.view.tintColor;
        }
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
        return cell;'''

        if old_cell in s_content:
            s_content = s_content.replace(old_cell, new_cell, 1)

        old_select = 'else if (indexPath.section == 2 && indexPath.row == 0) [self respring];\n    else if (indexPath.section == 2 && indexPath.row == 1) [self openLog];'
        new_select = '''else if (indexPath.section == 2 && indexPath.row == 0) [self respring];
    else if (indexPath.section == 2 && indexPath.row == 1) [self cleanCaches];
    else if (indexPath.section == 2 && indexPath.row == 2) [self openLog];'''

        if old_select in s_content:
            s_content = s_content.replace(old_select, new_select, 1)

        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(s_content)
        print("[+] SettingsVC.m patched with Cache Cleaner")

# 3. Update ru.lproj
ru_path = 'src/ru.lproj/Localizable.strings'
if os.path.exists(ru_path):
    with open(ru_path, 'r', encoding='utf-8') as f:
        ru_text = f.read()
    if 'Mute Shutter Sound' not in ru_text:
        with open(ru_path, 'a', encoding='utf-8') as f:
            f.write('''
"Mute Shutter Sound" = "Без звука затвора камеры";
"Camera Control Button" = "Кнопка Camera Control (16)";
"Lockscreen Dimming (LGLPM)" = "Затемнение экрана блокировки";
"iPad Apps on iPhone" = "iPad-приложения на iPhone";
"Clean App Caches" = "Очистить кэши приложений";
"Clean Caches?" = "Очистить кэши?";
"Delete temporary caches across app containers to free storage." = "Удалить временные файлы кэша из контейнеров приложений для освобождения места.";
"Cleaning caches..." = "Очистка кэша...";
"Cleaned %lu cache items across app containers." = "Очищено элементов кэша: %lu.";
"Cache Cleaned" = "Кэш очищен";
''')
        print("[+] ru.lproj updated")

# 4. Update en.lproj
en_path = 'src/en.lproj/Localizable.strings'
if os.path.exists(en_path):
    with open(en_path, 'r', encoding='utf-8') as f:
        en_text = f.read()
    if 'Mute Shutter Sound' not in en_text:
        with open(en_path, 'a', encoding='utf-8') as f:
            f.write('''
"Mute Shutter Sound" = "Mute Shutter Sound";
"Camera Control Button" = "Camera Control Button";
"Lockscreen Dimming (LGLPM)" = "Lockscreen Dimming (LGLPM)";
"iPad Apps on iPhone" = "iPad Apps on iPhone";
"Clean App Caches" = "Clean App Caches";
"Clean Caches?" = "Clean Caches?";
"Delete temporary caches across app containers to free storage." = "Delete temporary caches across app containers to free storage.";
"Cleaning caches..." = "Cleaning caches...";
"Cleaned %lu cache items across app containers." = "Cleaned %lu cache items across app containers.";
"Cache Cleaned" = "Cache Cleaned";
''')
        print("[+] en.lproj updated")

# 5. Update build.sh version
build_path = 'build.sh'
if os.path.exists(build_path):
    with open(build_path, 'r', encoding='utf-8') as f:
        b_content = f.read()
    b_content = b_content.replace('VERSION="2.5.2"', 'VERSION="2.5.3"')
    with open(build_path, 'w', encoding='utf-8') as f:
        f.write(b_content)
    print("[+] build.sh version bumped to 2.5.3")

# 6. Update Info.plist version
info_path = 'src/Info.plist'
if os.path.exists(info_path):
    with open(info_path, 'r', encoding='utf-8') as f:
        i_content = f.read()
    i_content = i_content.replace('<string>2.5.2</string>', '<string>2.5.3</string>')
    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(i_content)
    print("[+] Info.plist version bumped to 2.5.3")

print("[*] All patches applied successfully!")
